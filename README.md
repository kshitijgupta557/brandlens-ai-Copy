# BrandLens AI

An evidence-based multi-agent brand auditing application, being built in small milestones.

## What works now

Milestone 2 is a polished dashboard demonstration with a white/light-grey theme,
muted teal and gold accents, responsive KPI cards and interactive Altair charts.
The sidebar has seven pages: Brand Audit, Overview, Competitor Analysis, Consumer
Sentiment, Digital Presence, Strategic Recommendations and Reports.

**All scores, charts, peers and example interpretations are synthetic.** Entering
a real company name only labels your workspace; it does not make the fixtures
real findings about that company. No web research, model requests or live agent
execution occurs. The app does not write inputs to disk; workspace state is held
in the current Streamlit session and can reset on reload or server restart.

### Try the demo

1. Start the app using the instructions below. Overview opens with fictional data.
2. Choose **Brand Audit** in the sidebar and enter a company, market and category.
3. Check the demo acknowledgement, then click **Run demo audit**.
4. Explore the analysis pages. Changing company names does not change the fixtures.
5. On **Strategic Recommendations**, filter the sample agenda by planning horizon.
6. On **Reports**, download the Markdown blueprint. It has 12 planned sections,
   evidence requirements and a suggested ~18-slide presentation outline. It is
   **not a completed audit** and contains no mock findings. PDF, Word and PPTX
   exports are not implemented yet.

On a narrow screen, use Streamlit's sidebar control to open navigation. KPI cards
reflow to two columns and then one; charts resize with their containers.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Sidebar navigation and session workspace |
| `dashboard/views.py` | Seven dashboard screens |
| `dashboard/ui.py` | Reusable styling, headers and responsive cards |
| `dashboard/charts.py` | Interactive, inline-data Altair charts |
| `dashboard/demo.py` | Clearly synthetic, deterministic fixtures |
| `dashboard/report.py` | Detailed report blueprint and Markdown download |
| `.streamlit/config.toml` | Light theme and disabled usage telemetry; no secrets |
| `gemini.py` | Secret loading, provisional model ID, and disabled client factory |
| `requirements.txt` | Streamlit, Altair and Google's official `google-genai` SDK |
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
   http://localhost:8501. Explore Overview, then choose Brand Audit to set up a
   demo workspace. Keep the terminal open while using it.
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

## Streamlit Community Cloud compatibility

The entry point remains `app.py` at the repository root. Use Python 3.11 or 3.12
and install `requirements.txt`. All chart data and styles are local: no database,
external font, browser automation, paid service or additional system package is
required. No key is needed. Existing Community Cloud apps tracking `main` may
automatically pick up a new commit; this milestone creates no new deployment.

## Development checks

From the project root, run `python -m compileall -q app.py gemini.py dashboard`.
The dashboard has also been checked using Streamlit AppTest for navigation,
form validation, session persistence and recommendation filtering with model
client construction blocked. Gemini remains disabled in `gemini.py`.
