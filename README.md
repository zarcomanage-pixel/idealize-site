# idealizepalace.com

The Idealize website: plain HTML and CSS, no build step. Hosted on GitHub Pages (custom domain in `CNAME`).

- `index.html`: the homepage
- `privacy/`, `terms/`, `support/`: these must stay at the same addresses, because the App Store links to them
- `assets/`: styles, the night-sky script and images (screens come from the 2.0 App Store set)

To preview, run `python3 -m http.server` in this folder and open http://localhost:8000. Add `?theme=dark` or `?theme=light` to force a theme.
