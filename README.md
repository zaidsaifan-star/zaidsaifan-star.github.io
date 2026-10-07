# Zaid Saifan Portfolio

Personal engineering portfolio for **Zaid Saifan**, Electrical Engineering student at Western University.
Static HTML/CSS/JS, ready for GitHub Pages.

**Continuing in Claude Code?** Open this folder in Claude Code and say *"Read CLAUDE.md and publish this to GitHub Pages."*
`CLAUDE.md` has the full handoff: deploy commands, how the site is built, design rules and open items.

**Editing content:** page HTML is generated. Change text in `tools/build.py`, then run `python3 tools/build.py`.

## Put it online with GitHub Pages (about 5 minutes)

1. Create a GitHub account if you don't have one, then create a **new public repository**.
   - For the cleanest link, name it `YOUR-USERNAME.github.io` → the site will live at `https://YOUR-USERNAME.github.io`.
   - Any other name (e.g. `portfolio`) works too → `https://YOUR-USERNAME.github.io/portfolio`.
2. In the repo, click **Add file → Upload files** and drag in everything from this folder
   (`index.html`, `projects/`, `assets/`, `README.md`). Commit.
3. Go to **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**,
   branch **main**, folder **/ (root)**. Save.
4. Wait about a minute and open the link GitHub shows. Put that link on your résumé and LinkedIn.

## Add your headshot

Save a square photo as `assets/img/zaid.jpg` (about 400×400 px). It replaces the "ZS" initials in the hero automatically.

## Add project photos

Drop images into `assets/img/` and reference them in `tools/build.py`, then rebuild.
Good candidates: the golf cart power board render, RC car photos, Roboracer build photos, oscilloscope captures from the function generator.

## Update your résumé

Replace `assets/Zaid_Saifan_Resume.pdf` with your newest version (keep the same file name).

## Structure

```
index.html                     Home page (generated)
projects/*.html                One write-up per project (generated)
tools/build.py                 All page content; run it to regenerate the HTML
CLAUDE.md                      Handoff notes for Claude Code
assets/css/site.css            All styles (light + dark mode)
assets/js/site.js              Image zoom, copy-email button, headshot fallback
assets/img/                    Project images
assets/video/                  RC car demo videos
assets/Zaid_Saifan_Resume.pdf  Résumé linked from every page
```
