# Diffie-Hellman Key Exchange – Full-Stack Demo (Flask)

An interactive web app that demonstrates Diffie-Hellman (DH) key exchange and secure message communication.

- Compute public keys and the shared secret from inputs `p`, `g`, `a` (Alice), `b` (Bob).
- Encrypt/decrypt messages using a symmetric key derived from the shared secret (HKDF → Fernet).
- Clear, step-by-step UI with explanations.
- Backend: Python Flask. Frontend: HTML/CSS/JS.
- Deployable to Render, Heroku, or Vercel.

## Local Development

1) Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

2) Install dependencies:

```bash
pip install -r requirements.txt
```

3) Run the app:

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## How It Works

- Public keys:
  - `A = g^a mod p` (Alice)
  - `B = g^b mod p` (Bob)
- Shared secret (both sides):
  - `s = B^a mod p = A^b mod p = g^(ab) mod p`
- Symmetric key derivation:
  - HKDF-SHA256 derives a 32-byte key from `s` with salt `(p, g)` and info `diffie-hellman-demo`.
  - Converted to a Fernet key and used to encrypt/decrypt messages.

Endpoints:
- `POST /api/compute` → `{ A, B, s1, s2, match }`
- `POST /api/encrypt` → `{ ciphertext, shared_secret }` (sender: `alice` or `bob`)
- `POST /api/decrypt` → `{ plaintext, shared_secret }` (recipient: `alice` or `bob`)

Note: For transparency, the API returns `shared_secret`. Do not do this in production.

## Deploy to Render

- Commit this repository to GitHub/GitLab.
- In Render dashboard → New → Web Service.
- Connect the repo, choose `render.yaml` for auto configuration.
- Render will use:
  - Build: `pip install -r requirements.txt`
  - Start: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`

Alternatively, set these manually if not using `render.yaml`.

## Deploy to Heroku

- Ensure you have the Heroku CLI installed and are logged in.

```bash
git init
heroku create dh-diffie-demo
heroku stack:set heroku-22
heroku buildpacks:set heroku/python
git add .
git commit -m "Deploy DH demo"
git push heroku HEAD:main
```

Heroku will use `requirements.txt` and `Procfile`:
- `web: gunicorn wsgi:app`

## Deploy to Vercel

Vercel can run Python WSGI apps. Included `vercel.json` deploys `wsgi.py`.

Steps:
- Install Vercel CLI and log in: `npm i -g vercel && vercel login`
- From the project directory, run: `vercel --prod`

Vercel will use:
- `vercel.json` builds `wsgi.py` with `@vercel/python` and routes all paths to it.

Note: Cold starts may apply; for durable always-on servers, prefer Render or Heroku.

## Project Structure

```
.
├─ app.py               # Local dev entry
├─ wsgi.py              # WSGI entry for Gunicorn/Vercel
├─ requirements.txt
├─ Procfile             # Heroku
├─ render.yaml          # Render
├─ vercel.json          # Vercel
└─ app/
   ├─ __init__.py
   ├─ routes.py         # API endpoints and index route
   ├─ crypto_utils.py   # DH, HKDF, Fernet helpers
   ├─ templates/
   │  └─ index.html     # UI
   └─ static/
      ├─ css/styles.css
      └─ js/main.js
```

## Example Parameters

Try small numbers to see the flow:
- `p = 23`, `g = 5`, `a = 6`, `b = 15`

## Security Notes

- Educational demo only. Do not print or return secrets in real systems.
- Real-world DH uses large safe primes and validated generators, plus authentication to prevent MITM.
- For production, use TLS or authenticated key exchange (e.g., X25519 + AEAD with proper KDFs).
