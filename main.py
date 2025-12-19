"""
FastAPI backend for social media OSINT search

This API exposes an endpoint ``/search`` that accepts a JSON payload with a
``username`` and an optional list of ``sites``. It then calls the Sherlock
command‑line tool to hunt for accounts on social media.  The results are
returned as a JSON object containing the found URLs.  If Sherlock is not
installed or fails, a clear error message is returned.

Example request:

.. code-block:: json

   POST /search
   {
     "username": "exampleuser",
     "sites": ["twitter", "instagram"]
   }

``requirements.txt`` lists the Python dependencies necessary to run this
server.  To start the server locally, install the dependencies and run
``uvicorn main:app --reload``.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import re
from typing import List, Optional


app = FastAPI(
    title="Social OSINT API",
    description=(
        "This API wraps the Sherlock command‑line tool to search for "
        "social media profiles associated with a given username. It returns a list "
        "of URLs where the username was found."
    ),
    version="0.1.0",
)


class SearchRequest(BaseModel):
    """Payload for the search request."""

    username: str
    sites: Optional[List[str]] = None


@app.post("/search")
async def search_profiles(req: SearchRequest):
    """Search for social media profiles using the Sherlock CLI.

    Args:
        req: JSON payload containing ``username`` and optional ``sites``.

    Returns:
        A mapping of the username to a list of URLs where the account was found.
    """
    username = req.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username must not be empty")

    # Construct the Sherlock command.
    # ``--print-found`` limits output to found results only; this makes parsing easier.
    cmd: List[str] = ["sherlock", username, "--print-found"]
    # Add individual site filters if provided
    if req.sites:
        for site in req.sites:
            # Sherlock CLI expects each ``--site`` argument separately.
            cmd.extend(["--site", site])

    try:
        # Run Sherlock. We capture stdout so we can parse results.  We do not
        # raise on non-zero return codes since Sherlock exits with non-zero
        # when some sites fail but others succeed.
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # Sherlock is not installed; instruct the user how to install it.
        raise HTTPException(
            status_code=500,
            detail=(
                "Sherlock CLI is not installed on the server. Install it via "
                "`pip install sherlock-project` or run this API on a host where "
                "Sherlock is available."
            ),
        )

    # Parse the output for URLs. Sherlock prints lines like:
    # "[+] Twitter: https://twitter.com/exampleuser"
    found_links: List[str] = []
    for line in result.stdout.splitlines():
        match = re.search(r"https?://\S+", line)
        if match:
            found_links.append(match.group(0))

    return {"username": username, "links": found_links}