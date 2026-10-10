# BrandLens AI

An evidence-based multi-agent brand auditing application, being built in small milestones.

## What works now

This first milestone displays the app title and a company-name input. It checks
whether a Gemini key is configured, without showing or validating the key.
It does not research companies, generate audits, save company names to disk,
or send company names to Google. Agents and evidence collection come later.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | The Streamlit screen |
| `gemini.py` | Secret loading, provisional model ID, and disabled client factory |
| `requirements.txt` | Streamlit and Google's official `google-genai` Python SDK |
| `.gitignore` | Keeps local secrets and temporary files out of Git |

## Run on your own computer (no deployment)

An API key is **not needed** for this milestone. Nothing here enables billing.

1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/.
   On Windows, select **Add Python to PATH** in the installer.
2. Open this private repository in GitHub while signed in. Click **Code → Download ZIP**.
   Extract the ZIP, then open the folder that contains `app.py`.
3. Open a terminal in that folder. On Windows, click the File Explorer address
   bar, type `powershell`, and press Enter. A terminal is a window where you run
   the commands below. Enter only the contents of each code block, without its
   surrounding backticks.
4. Create an isolated Python environment, which keeps project packages separate:

   **Windows PowerShell**
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe -m streamlit run app.py --browser.gatherUsageStats false
   ```

   **macOS / Linux terminal**
   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python -m streamlit run app.py --browser.gatherUsageStats false
   ```

5. Open the local address printed in the terminal, normally
   http://localhost:8501. Type a company name. The app should show a message
   explaining that audits are not enabled. Keep the terminal open while using it.
6. Press **Ctrl+C** in the terminal to stop. To start again, run only the last
   command for your operating system. If `requirements.txt` cannot be found,
   check that your terminal is in the folder containing that file.

## Optional secret setup (not required now)

Never paste a real key into ChatGPT, the README, Python source, or a GitHub commit.
If you already have a key, you may store it **only on your own computer**:

1. In the project folder, create a folder called `.streamlit`.
2. Inside it, create a text file called `secrets.toml` (not `secrets.toml.txt`).
3. Add the following line, replacing the placeholder privately:

   ```toml
   GEMINI_API_KEY = "YOUR_KEY_HERE"
   ```

4. Restart the app. A detected key does not mean it is valid or has model access.

Alternatively, provide an operating-system environment variable named
`GEMINI_API_KEY` to the process running Streamlit. A nonempty environment value
takes precedence over Streamlit Secrets. Blank, missing, or invalid secrets are
treated as unconfigured. `.env` files are ignored by Git but are **not loaded**
automatically by this scaffold. Both `.env` and `.streamlit/secrets.toml` are
already excluded in `.gitignore`; never force-add them to Git.

## Gemini model and request safety

- Provisional selection: **Gemini 3.5 Flash-Lite**.
- Exact documented API identifier: `gemini-3.5-flash-lite`, checked on 2026-10-10
  against https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash-lite.
- Official SDK: https://googleapis.github.io/python-genai/.
- `API_REQUESTS_ENABLED = False` blocks client creation. The app contains no
  generation requests and never calls the client factory.
- No paid services, billing setup, or deployment are part of this milestone.
- Before implementing requests in a later milestone, recheck the identifier,
  account availability, and applicable free-tier quotas. Documentation verification
  does not verify access for an individual API key or guarantee free usage.

Dependency ranges allow compatible releases; this scaffold does not yet include
a fully locked dependency environment.
