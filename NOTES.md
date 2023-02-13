## Running

1. Clone the repo and change directory into the newly created source root
2. Create a Python virtual environment: `python3 -m venv ./venv`
3. Install the requirements: `./venv/bin/pip install -r requirements.txt`
4. Copy the sample configuration file: `cp config.py.SAMPLE config.py`, then in `config.py`:
    1. Generate a new Flask secret key: `./venv/bin/python -c 'import os; print(os.urandom(32))'`, then assign this value to `SECRET_KEY`
    2. Assign your Giant Bomb API key to `GIANTBOMB_API_KEY`
5. Run the application: `./run.py`
6. Navigate to the site at http://127.0.0.1:5000/


## Caveats

This webapp was created to remain within the time box of ~4 hours, and thus contains several compromises, poor or hacky decisions, and deficiencies.

Some are listed below:

- No data persistence
- No user auth (a fake user is always "logged in")
- UI has inconsistent design paradigm -- most pages are server-side rendered, but some client-side actions occur (e.g. adding games to the cart)
- When a game is added to the cart, the page refreshes (to update cart count) even though we're adding it via `fetch`
- There is no way to remove games from the cart (other than checking out)
- "Checkout" simply empties the cart with a message of success
- Games in cart are sorted by GUID instead something more human-friendly like game title
- You can still click games already in cart, which doesn't duplicate them, but runs the logic and reloads the page unnecessarily
- No errors are handled (either internal or Giant Bomb API errors)
- Other than the HTML templates, the structure of the app is not well organized, particularly on the view-side of things
- The Giant Bomb API client could request less game data since we're only using a small subset
- Giant Bomb API code could be better designed
- No proper "landing page" -- should support an empty search page
- No tests
- No caching
- Not too many code comments
- HTML and CSS are rushed and suboptimal
- Tested on Firefox 109.0 on Ubuntu 20.04.5 LTS, and nothing else
- Git commits are poorly not well structured
