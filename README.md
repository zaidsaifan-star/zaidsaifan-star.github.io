# Zaid Saifan · Electrical Engineering Portfolio

Personal portfolio for **Zaid Saifan**, Electrical Engineering student at Western University (London, ON).
PCB and power distribution design, controls, robotics and embedded systems.

Static HTML/CSS/JS. No framework, no build step. Ready for **GitHub Pages**.

## What's in it

| Section | What it shows |
| --- | --- |
| Hero | Animated circuit-board background with current pulses, typed role line, PCB "drawing" with title block |
| At a glance | Count-up stats: 81.3 % Year 2 average, 15–20 A power board, 140 h internship, 6 projects |
| What I do | Power & PCB design · Controls & robotics · Building electrical design |
| Projects | 6 write-ups with category filters (PCB & Power, Robotics & Controls, Circuits & Logic) |
| Experience | Scroll-linked timeline: Dr. Zaki Research Lab, Epsilon Engineers & Architects, Western Engineering AutoPilot |
| Skills | Education card with grade gauges, grouped skill chips |
| Contact | Email (with copy button), phone, LinkedIn, résumé |

Each project page reads like a datasheet: role, key-spec table, numbered figures with a full-size lightbox,
wiring diagrams that draw themselves in, results and videos.

**Effects:** circuit-trace canvas that glows near the cursor, letter-by-letter name reveal, typed text,
scroll-reveal with stagger, 3D card tilt, cursor spotlight on cards, magnetic buttons, scroll progress bar,
active-section nav indicator, animated timeline, gauges and counters, infinite tool marquee, back-to-top ring.
Dark and light themes (toggle in the header, remembered per visitor). All motion turns off for visitors who
have *reduce motion* enabled in their OS.

## Publish on GitHub Pages (about 5 minutes)

1. Create a **new public repository** on GitHub.
   - Name it `YOUR-USERNAME.github.io` for the cleanest link: `https://YOUR-USERNAME.github.io`
   - Any other name (e.g. `portfolio`) also works: `https://YOUR-USERNAME.github.io/portfolio`
2. Upload everything in this folder (`index.html`, `projects/`, `assets/`, `.nojekyll`, `README.md`) and commit.
   With git: `git remote add origin https://github.com/YOUR-USERNAME/REPO.git` then `git push -u origin main`.
3. In the repo go to **Settings → Pages → Build and deployment**, choose **Deploy from a branch**,
   branch **main**, folder **/ (root)**, and save.
4. After about a minute, open the link GitHub shows. Put it on your résumé and LinkedIn.

All links are relative, so the site works at either URL with no changes.

## Editing

- **Text and projects:** edit `index.html` and the pages in `projects/` directly.
- **Colours and fonts:** design tokens are at the top of `assets/css/site.css` (dark theme in `:root`, light theme in `:root[data-theme="light"]`).
- **Effects:** `assets/js/site.js`. The site still reads fine with JavaScript off.
- **Résumé:** replace `assets/Zaid_Saifan_Resume.pdf` (keep the file name).
- **Photos:** add `.webp` images to `assets/img/` (about 1600 px on the long side).
- `tools/build.py` is the generator for the *previous* design. It no longer matches these pages; don't run it unless you port the new templates into it.

## Structure

```
index.html                     Home page
projects/*.html                One write-up per project
assets/css/site.css            All styles (dark + light themes)
assets/js/site.js              Effects and interactions
assets/img/                    Project images
assets/video/                  RC car demo videos
assets/Zaid_Saifan_Resume.pdf  Résumé linked from every page
github-profile/README.md       Optional profile README for github.com/YOUR-USERNAME
.nojekyll                      Tells GitHub Pages to serve files as-is
```
