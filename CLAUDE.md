# Zaid Saifan Portfolio — handoff for Claude Code

Static personal portfolio site for **Zaid Saifan**, Electrical Engineering student at Western University (London, ON).
Audience: co-op / internship recruiters. Plain HTML/CSS/JS, no framework, no npm, no build server. Deploys to **GitHub Pages**.

## First task: publish to GitHub Pages

The site is finished and ready to ship. Goal: a public repo with Pages enabled, then give Zaid the live URL.

1. Check the GitHub CLI: `gh auth status`. If not logged in, run `gh auth login` (GitHub.com → HTTPS → browser) and let Zaid finish in the browser.
2. Ask Zaid which repo name he wants:
   - `<username>.github.io` → site at `https://<username>.github.io/` (recommended, cleanest link for a résumé)
   - anything else, e.g. `portfolio` → site at `https://<username>.github.io/portfolio/`
   All links in the site are relative, so both work with no code changes.
3. This folder is already a git repo with one commit on `main`. Create and push:
   ```bash
   gh repo create <repo-name> --public --source=. --remote=origin --push
   ```
4. Turn on Pages from the `main` branch root:
   ```bash
   gh api -X POST repos/<username>/<repo-name>/pages -f "source[branch]=main" -f "source[path]=/"
   ```
   (If it says Pages already exists, use `-X PUT` instead.) `.nojekyll` is already in the repo so files are served as-is.
5. Wait ~1 minute, check `gh api repos/<username>/<repo-name>/pages --jq .html_url`, open it, and confirm the home page, one project page, the images, the videos and the résumé PDF all load.
6. Optional: set the repo description and website URL:
   `gh repo edit --description "Electrical engineering portfolio – Zaid Saifan" --homepage <pages-url>`

## Repo layout

```
index.html                    GENERATED – home page
projects/*.html               GENERATED – one datasheet-style page per project
tools/build.py                Source of truth for ALL page content + inline SVG diagrams
assets/css/site.css           Hand-written styles (design tokens at the top, light + dark mode)
assets/js/site.js             Image lightbox, copy-email button, headshot fallback, footer year
assets/img/                   Project images (.webp)
assets/video/                 RC car videos (.mp4, H.264, no audio) + poster frames
assets/Zaid_Saifan_Resume.pdf Résumé linked from the nav and every page
.nojekyll                     Tells GitHub Pages to skip Jekyll
```

**Never hand-edit `index.html` or `projects/*.html`.** Edit `tools/build.py`, then run `python3 tools/build.py`
(Python 3, standard library only) and commit both the script and the regenerated HTML.

In `build.py`:
- `P` is the list of projects (order = order on the home page). Each has `slug, title, short, eyebrow, lede, card, role, tags, thumb, specs, hero, results, sections`, plus optional `gallery`, `gallery_title`, `videos`, `note`.
- `thumb` / `hero` are `("img", "file.webp", "alt/caption")` or `("svg", svg_function, "caption")`.
- `gallery` entries are `(file, caption, unused_flag)`; images under `hospital-*` get a dark backdrop.
- `build_index()` holds the hero, facts strip, experience, education and skills HTML.
- Contact details are constants at the top (`EMAIL`, `PHONE`, `LINKEDIN`).

## Design system (keep it consistent)

Concept: an engineering datasheet — title block in the hero, key-spec tables, numbered figures.
- Fonts (Google Fonts): Red Hat Display (headings), Red Hat Text (body), Red Hat Mono (labels/data).
- Colours are CSS custom properties at the top of `site.css`; every colour must come from a token and be defined for light (`:root`) and both dark blocks.
  - `--copper` #A9501B (accent, links, highlights)
  - `--mask` #1F3A5F navy (secondary: tags, spec-table headers, logo mark) — **changed from green at Zaid's request; don't bring green back**
  - cool blue-grey neutrals for paper/panel/ink/line
- The favicon in `build.py` (`FAVICON`) uses the navy `%231F3A5F`.
- Add images as `.webp` (≈1600 px long side, quality ~82). Videos: H.264 MP4, `-an`, `-movflags +faststart`.

## Facts (source: Zaid's résumés — don't invent numbers)

- B.E.Sc. Electrical Engineering, Western University, expected April 2029. Year 2 avg 81.3%, cumulative 76.3%, Dean's Honor List 2025–26. Available for 12–16 month co-op from May 2027.
- Email zaid.saifan06@gmail.com · Phone (905) 617-1304 · LinkedIn https://www.linkedin.com/in/zaid-saifan-0b369b356
- Experience: Dr. Zaki Research Lab (Undergrad RA, Sep 2026–present: Roboracer PDB, LiDAR/IMU SLAM, Clearpath Husky wiring); Epsilon Engineers & Architects, Amman (EE Intern, Jun–Jul 2026, 140 h: load calcs, cable sizing, AutoCAD/Revit drawings); Western Engineering AutoPilot (Oct 2025–present: PWM throttle control, golf cart PDB co-design, RC car).
- Golf cart PDB was co-designed with teammate **Abdelrahman** (board silkscreen: "Zaid & Abdelrahman"). Keep the "co-design / contributed" wording.

## Open items to ask Zaid about

1. **RC car battery:** the page says "11.1 V 3S LiPo", but the photos show a green 2800 mAh pack. Confirm the real battery and fix `specs` + the "Power and motor hardware" section.
2. **FPGA Sequence Detector** and **Analog Function Generator** aren't on his résumé. Confirm he built his own versions; remove them from `P` if not.
3. **Headshot:** save a square photo as `assets/img/zaid.jpg` (~400×400). It automatically replaces the "ZS" initials in the hero.
4. **Roboracer photos:** that page still uses a drawn SVG diagram. Add photos when he has them.
5. Optional: a social preview image (`og:image`) once the final URL is known.

## Checks before every push

- `python3 tools/build.py` runs clean.
- No horizontal scroll at 390 px wide; light and dark mode both readable.
- All `assets/...` paths resolve (relative links only — no leading `/`, so project-repo URLs keep working).
