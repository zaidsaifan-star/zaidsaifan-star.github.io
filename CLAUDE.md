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
index.html                    Home page (hand-edited)
projects/*.html               One datasheet-style page per project (hand-edited)
assets/css/site.css           Styles; design tokens at the top (dark default + light theme)
assets/js/site.js             Effects: circuit canvas, reveals, tilt, filters, counters, timeline, lightbox, theme toggle
assets/img/                   Project images (.webp)
assets/video/                 RC car videos (.mp4, H.264, no audio) + poster frames
assets/Zaid_Saifan_Resume.pdf Résumé linked from the nav and every page
github-profile/README.md      Optional GitHub profile README (replace YOUR-USERNAME)
tools/build.py                LEGACY generator for the previous design — out of date, do not run
.nojekyll                     Tells GitHub Pages to skip Jekyll
```

The 2026-10 redesign was written directly as HTML (no Python on that machine), so the HTML is now the
source of truth. The header and contact/footer blocks are identical across all 7 pages: change them everywhere.
Project pages wrap the crumbs + `.ds-head` in `<section class="page-hero">` with a `<canvas class="hero-canvas">`.

## Design system (keep it consistent)

Concept: a powered-up circuit board — midnight solder-mask background, copper traces that glow, datasheet details.
- Fonts (Google Fonts): Space Grotesk (headings), Inter (body), JetBrains Mono (labels/data).
- Colours are CSS custom properties at the top of `site.css`; dark in `:root`, light in `:root[data-theme="light"]`.
  - `--copper` #F08A4B dark / #B4561E light (accent, links, highlights)
  - `--mask` #7FB0FF dark / #1F4A85 light (secondary blue: tags, logic rails) — **no green accents (Zaid's request)**
- Animations add `data-reveal` (scroll reveal), `.spot` (cursor glow), `.tilt` (3D tilt), `.magnetic` (buttons).
  Project-page blocks get `data-reveal` automatically in `site.js`. Everything respects `prefers-reduced-motion`.
- Home-page project cards carry `data-cat` (`pcb`, `robotics`, `circuits`) for the filter; keep filter counts in sync.
- Add images as `.webp` (≈1600 px long side, quality ~82). Videos: H.264 MP4, `-an`, `-movflags +faststart`.

## Facts (source: Zaid's résumés — don't invent numbers)

- B.E.Sc. Electrical Engineering, Western University, expected April 2029. Year 2 avg 81.3%, cumulative 76.3%, Dean's Honor List 2025–26. Available for 12–16 month co-op from May 2027.
- Email zaid.saifan06@gmail.com · Phone (905) 617-1304 · LinkedIn https://www.linkedin.com/in/zaid-saifan-0b369b356
- Experience: Dr. Zaki Research Lab (Undergrad RA, Sep 2026–present: Roboracer PDB, LiDAR/IMU SLAM, Clearpath Husky wiring); Epsilon Engineers & Architects, Amman (EE Intern, Jun–Jul 2026, 140 h: load calcs, cable sizing, AutoCAD/Revit drawings); Western Engineering AutoPilot (Oct 2025–present: PWM throttle control, golf cart PDB co-design, RC car).
- Golf cart PDB was co-designed with teammate **Abdelrahman** (board silkscreen: "Zaid & Abdelrahman"). Keep the "co-design / contributed" wording.

## Open items to ask Zaid about

1. **RC car battery:** the page says "11.1 V 3S LiPo", but the photos show a green 2800 mAh pack. Confirm the real battery and fix `specs` + the "Power and motor hardware" section.
2. **FPGA Sequence Detector** and **Analog Function Generator** aren't on his résumé. Confirm he built his own versions; remove them from `P` if not.
3. **Headshot:** the redesign has no photo slot. If Zaid wants one, add it to the hero (e.g. inside `.status` row) as `assets/img/zaid.jpg`.
4. **Roboracer photos:** that page still uses a drawn SVG diagram. Add photos when he has them.
5. Optional: a social preview image (`og:image`) once the final URL is known.

## Checks before every push

- No horizontal scroll at 390 px wide; light and dark mode both readable.
- All `assets/...` paths resolve (relative links only — no leading `/`, so project-repo URLs keep working).
