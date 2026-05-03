🇬🇧 **[English version](README.md)**

<div align="center">

<img src="docs/images/logo-readme.svg" alt="Stilisierte Figur mit Euromünzen als Brille." width="100" height="65" />

# ISTA EcoTrend Reporter

[![ISTA EcoTrend Reporter](https://img.shields.io/badge/GitHub_Actions-ISTA_EcoTrend_Reporter-2088FF?logo=githubactions&logoColor=white)](https://github.com/gabrielbahniuk/ista-ecotrend-exporter/actions/workflows/report.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

<!-- ista-report-nav:begin -->
<h3 align="center"><a href="./generated/reports/REPORT.md">Neuesten Report öffnen →</a></h3>
<p align="center"><sup>Zuletzt erstellt · 03.05.2026 11:51</sup></p>
<!-- ista-report-nav:end -->

Die ISTA-EcoTrend-App fasst Heiz- und Warmwasserverbrauch übers Jahr zusammen. Dieses Template nutzt GitHub Actions für denselben Loginweg wie die App und committet Markdown-Reports, Charts und eine CSV unter `generated/`. Ein privates Repo hält die Daten aus dem öffentlichen Internet.

![Demo: Einrichtung und Reports ansehen](docs/report-demo.gif)

## Schnellstart

1. **Use this template** → **Create a new repository**.
2. Namen und optional Beschreibung wählen, Sichtbarkeit **Private** empfohlen.
3. **Settings** → **Secrets and variables** → **Actions**.
4. Zwei Repository-Secrets anlegen (Namen exakt):

   | Name | Wert |
   |------|------|
   | `ISTA_EMAIL` | deine ISTA-EcoTrend-Login-E-Mail |
   | `ISTA_PASSWORD` | Passwort dieses Kontos |

5. Tab **Actions** → Workflow **ISTA EcoTrend Reporter**.
6. **Run workflow** → Branch (meist `main`) → **Run workflow**.

Nach dem Push: **`generated/reports/REPORT.md`** auf dem Branch öffnen oder **`generated/reports/`** für Index und Jahresdateien durchsuchen.

Runs, die du mit **Run workflow** startest, zeigen zusätzlich im **Summary** des Workflow-Laufs einen Direktlink zu `REPORT.md`. **Geplante** Läufe (`schedule`) führen diesen Summary-Schritt nicht aus (`workflow_dispatch`-Bedingung in [.github/workflows/report.yml](.github/workflows/report.yml)); dann Dateibaum oder `REPORT.md` öffnen, oder Workflow anpassen.

### Zeitplan

Derselbe Workflow läuft am **18. jedes Monats um 06:00 UTC**. Cron in [.github/workflows/report.yml](.github/workflows/report.yml) anpassen. Die ISTA-Verbrauchs-Mail kommt oft zwischen dem **13. und 16.**

<details>
<summary>Optional: Screenshots zur GitHub-Oberfläche (SVG-Platzhalter in <code>docs/tutorial/</code> gegen echte Aufnahmen tauschen)</summary>

**Settings** → **Secrets and variables** → **Actions**:

![Platzhalter: Repository-Secrets](docs/tutorial/readme-tutorial-secrets.svg)

**Actions** → **ISTA EcoTrend Reporter** → **Run workflow**:

![Platzhalter: Run workflow](docs/tutorial/readme-tutorial-run-workflow.svg)

Nach manuellem Run: letzter Lauf → **Summary** (Link zu `REPORT.md` nur bei manuellem Dispatch):

![Platzhalter: Job-Summary mit Link](docs/tutorial/readme-tutorial-summary-link.svg)

</details>

## Disclaimer

- Daten über die **inoffizielle** Bibliothek **`pyecotrend-ista`** ([Upstream](https://github.com/Ludy87/pyecotrend-ista); Git-Pin in [`requirements.txt`](requirements.txt)). ISTA kann Schnittstellen oder Bedingungen ändern. Nutzung auf eigenes Risiko.
- Kein offizielles ISTA-Produkt, keine gehostete Datenbank und kein Echtzeit-Dashboard. Nur Automation, die Reports in dein Repo committet.
- **`ISTA_EMAIL`** / **`ISTA_PASSWORD`** niemals in Issues oder Screenshots offenlegen.

## Lokal (optional)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
cp .env.example .env
# .env bearbeiten: ISTA_EMAIL und ISTA_PASSWORD
set -a && source .env && set +a
python -m src.pipeline.report
```

| Variable | Zweck |
|----------|-------|
| `ISTA_EMAIL`, `ISTA_PASSWORD` | ISTA-Login für Live-API |

```bash
python -m pytest -q
```

## Sicherheit

- Niemals `.env` oder Zugangsdaten versionieren.
- ISTA-Passwort rotieren, falls es geleakt sein könnte.
- **Privates** Repository, wenn Verbrauchsdaten nicht öffentlich sein sollen.
