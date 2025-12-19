// Front‑end script for Social OSINT (Option 2)
//
// This script sends the username to the FastAPI backend and displays
// whatever profile links are returned.  It uses fetch with JSON and updates
// the DOM dynamically.

// Change this to the URL where your FastAPI server is hosted.  When testing
// locally, use http://localhost:8000.  When deployed on a platform like
// Render, replace with your service’s URL.
const apiBaseUrl = 'http://localhost:8000';

const form = document.getElementById('searchForm');
const usernameInput = document.getElementById('username');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = usernameInput.value.trim();
    if (!username) {
        statusEl.textContent = 'Please enter a username.';
        return;
    }
    statusEl.textContent = 'Searching…';
    resultsEl.innerHTML = '';
    try {
        const response = await fetch(`${apiBaseUrl}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username })
        });
        const data = await response.json();
        statusEl.textContent = '';
        if (!response.ok) {
            // API returned an error object
            statusEl.textContent = data.detail || 'Search failed.';
            return;
        }
        if (Array.isArray(data.links) && data.links.length > 0) {
            data.links.forEach((link) => {
                const li = document.createElement('li');
                const anchor = document.createElement('a');
                anchor.href = link;
                anchor.textContent = link;
                anchor.target = '_blank';
                li.appendChild(anchor);
                resultsEl.appendChild(li);
            });
        } else {
            statusEl.textContent = 'No profiles found.';
        }
    } catch (err) {
        statusEl.textContent = 'Error: ' + err.message;
    }
});