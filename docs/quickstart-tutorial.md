# Quick start — visual walkthrough

This doc mirrors the numbered steps from the README, with space for screenshots or GIFs per step.

**Screenshots vs GIFs**

| Approach | Effort | Best for |
|----------|--------|----------|
| **Six still PNGs** (one per step) | Medium | Highest clarity — readers pause on each GitHub UI state |
| **Two short GIFs** (Secrets flow + Actions run → success) | Low–medium | Good compromise; less file sprawl |
| **One long GIF** of the whole flow | Low | Faster to produce, easier to skim past details |

Nothing here is strictly required—the text steps in the README are enough for many people. Adding visuals mainly helps Reddit or friends who rarely use GitHub.

**Replacing placeholders:** drop PNGs/GIFs into [`docs/images/`](images/) using the filenames suggested under each step (same base name), or substitute your own filenames and edit the markdown.

---

### Step 1 — Fork this repository

1. Go to the upstream repo on GitHub.
2. Click **Fork** → choose destination account/org.
3. Turn on **private** if you do not want public consumption reports.

![Step 1 placeholder](images/quickstart-step-01-fork.svg)

*Replace with:* `quickstart-step-01-fork.png` — **Fork** button and dialog (redact repo list if shown).

---

### Step 2 — Open Actions secrets settings

In **your fork**: **Settings** → **Secrets and variables** → **Actions**.

![Step 2 placeholder](images/quickstart-step-02-secrets-location.svg)

*Replace with:* left sidebar highlighting **Secrets and variables**.

---

### Step 3 — Add `ISTA_EMAIL` and `ISTA_PASSWORD`

1. **New repository secret** → Name `ISTA_EMAIL`, value your ISTA login email → **Add secret**.
2. Repeat for `ISTA_PASSWORD`.

![Step 3 placeholder](images/quickstart-step-03-add-secrets.svg)

*Replace with:* list view showing both secret names (never show secret **values** in screenshots).

---

### Step 4 — Ensure Actions can run on the fork

**Settings** → **Actions** → **General**.

Allow **Actions** and **workflow permissions** suitable for forks (often “Read and write” for `GITHUB_TOKEN` on the workflow is already set in `.github/workflows/report.yml`; if the run fails to push commits, revisit this tab).

![Step 4 placeholder](images/quickstart-step-04-actions-settings.svg)

*Replace with:* policy section where forks allow workflows.

---

### Step 5 — Run the workflow manually

1. Tab **Actions** → workflow **Generate ISTA report**.
2. **Run workflow** → branch (usually default) → **Run workflow**.
3. Wait for the green check (open the job to see logs if it fails).

![Step 5 placeholder](images/quickstart-step-05-run-workflow.svg)

*Replace with:* dropdown confirmation or succeeded run overview.

---

### Step 6 — View the generated reports

1. In **Code**, open **`REPORT.md`** — links to yearly files.
2. Open e.g. **`REPORT_2026.md`** and scroll to **Charts** / tables.
3. SVG charts live under **`assets/charts/`**.

![Step 6 placeholder](images/quickstart-step-06-open-report.svg)

*Replace with:* browser view of markdown preview on GitHub (redact sensitive numbers if public).
