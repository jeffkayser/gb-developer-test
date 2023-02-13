import math
from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
import config
from . import giantbomb


GUID_SEPARATOR = "/"
DEFAULT_USERNAME = "Demo User"

app = Flask(__name__)
app.config.from_object(config)


def calc_page(offset, total, limit):
    return {"page_current": offset // limit + 1, "page_total": math.ceil(total / limit)}


def get_guids(req):
    guids = req.cookies.get("guids")
    if guids:
        guids = set(guids.split(GUID_SEPARATOR))
    else:
        guids = set()
    return guids


@app.route("/")
def index():
    return redirect(url_for(".search", query="mario"))


@app.route("/search/<string:query>/page/<int:page_num>")
@app.route("/search/<string:query>")
def search(query=None, page_num=1):
    guids = get_guids(request)
    if page_num < 1:
        page_num = 1
    r = giantbomb.search(
        query, api_key=app.config["GIANTBOMB_API_KEY"], page_num=page_num
    )
    results = r.json()
    meta = calc_page(
        results["offset"], results["number_of_total_results"], results["limit"]
    )
    meta.update({"query": query, "guids": guids, "username": DEFAULT_USERNAME})
    return render_template("search.html.jinja2", results=results, meta=meta)


@app.route("/cart/<string:guid>", methods=["POST"])
def cart(guid):
    guids = get_guids(request)
    guids.add(guid)
    resp = make_response("", 204)
    resp.set_cookie("guids", GUID_SEPARATOR.join(guids))
    return resp


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    guids = get_guids(request)
    games = giantbomb.get_games(guids, api_key=app.config["GIANTBOMB_API_KEY"])
    if request.method == "POST":
        resp = make_response(redirect(url_for(".checkout")))
        print("NEW RESP")
        resp.delete_cookie("guids")
        print("DELETE COOKIE")
        flash(
            f"Successfully checked out {len(games)}"
            f" game{'' if len(games) == 1 else 's'}. Thank you!"
        )
    else:
        resp = make_response(
            render_template(
                "checkout.html.jinja2",
                games=games,
                meta={"username": DEFAULT_USERNAME, "guids": guids},
            )
        )
    return resp
