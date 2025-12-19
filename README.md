# Social OSINT API (Option 2 – FastAPI)

This directory contains both a **FastAPI** backend and a minimalist **hack‑theme**
front‑end to run username searches across multiple social networks.  It uses the
open‑source [Sherlock project](https://github.com/sherlock-project/sherlock)
to perform the actual lookups.

## Contents

* `main.py` – FastAPI server wrapping the Sherlock CLI.  Defines a single
  `/search` endpoint that accepts JSON in the form `{ "username": "...", "sites": ["twitter", ...] }` and returns the links where the username was found.
* `requirements.txt` – Python dependencies for the server.
* `frontend/` – Static files (HTML, CSS, JavaScript) for the user interface.

## Running locally

1. **Install Python dependencies**

   ```sh
   pip install -r requirements.txt
   # You also need Sherlock – install via pip and ensure it's in your PATH
   pip install sherlock-project
   ```

2. **Start the API server**

   ```sh
   uvicorn main:app --reload
   ```

   The server will be available at `http://localhost:8000`.

3. **Serve the front‑end**

   Open the `frontend/index.html` file directly in your browser for local testing,
   or deploy the `frontend` folder to GitHub Pages.  Edit `app.js` to point
   `apiBaseUrl` at your running server (e.g. `http://localhost:8000`).

## Deploying to a free platform (Render)

To make your API publicly accessible on a zero‑cost tier, you can use
[Render.com](https://render.com/).  Create a new **Web Service** and point it
at this repository.  In your service settings, specify `uvicorn main:app --port
$PORT` as the start command.  Make sure to add `sherlock-project` to the
dependencies in `requirements.txt` before deployment.

## Notes

* The server uses the Sherlock command‑line tool via `subprocess.run()`.  If
  Sherlock is not installed, the API will return a 500 error with guidance.
* The front‑end uses a clean dark “hacker” theme with neon accents.
* Consider adding caching and request rate‑limiting if you expose this API
  publicly to prevent abuse.