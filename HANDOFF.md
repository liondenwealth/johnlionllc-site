# Studio website: where we stopped (2026-10-18)

Goal: turn johnlionllc.com into a PlayStation-style "app library": dark look, a featured-app carousel, a grid of portrait cover art for every app with tabs (All / Out now / Coming soon), and a page per app. Take the layout idea only: never PlayStation's logo, colours or wording. The user liked the PlayStation look and wants the covers like game covers.

## Done (local only, not pushed, nothing live changed)
- `tools/apps.json`: the 7 apps (Sono Bestie, Out The Chat, Back 2 The Past, XAELO BOX, Bearings, Card Wallet, The Lost Library) with tagline, status, accent colour, blurb, features, icon source path.
- `tools/make_covers.py`: builds `img/icons/<slug>.png`, `img/covers/<slug>.jpg` (600x800) and `img/hero/<slug>.jpg` (1600x900) from each app's icon. Run `python3 tools/make_covers.py`. Covers and hero checked by eye, they look right.

## Also done (2026-10-18, local only)
- `styles.css` dark-only + library styles; `tools/build.py` generates `index.html` and `apps/<slug>/index.html` (run `python3 tools/build.py` after editing apps.json); Sono Bestie shots in `img/shots/sono-bestie/`; /timeflies/ renamed to Back 2 The Past. Previewed desktop + phone, no console errors.

## Next
1. privacy.html and support.html still say "Time Flies, Meep, XAELO BOX and Bearings": update names/app list (legal text, confirm wording with user).
2. Check the other app pages and /timeflies/ by eye; ASK THE USER before `git push` (public repo liondenwealth/johnlionllc-site, main; live in minutes).

## Rules
- Do not say an app is "out" or give an App Store button until it is live. Sono Bestie is in Apple review (submitted 2026-10-16, build 35); when it goes live set its status to `out` and add its App Store link (id 6820216499).
- Out The Chat: no safety promises anywhere. Its own papers say it supplements 911 and venue security, and nobody (lawyer, security expert) has reviewed it yet. Keep "In testing".
- The user wants one chat per area so apps don't get mixed: Sono Bestie has its own chat; this website is a separate chat.
- Contact is support@johnlionllc.com. Follow-links for TikTok/Instagram only once accounts are confirmed (Sono Bestie's Instagram is @sonobestie).

## Related
- Calendar pages (content plans): Sono Bestie https://claude.ai/artifact/N71pxoxAesRi9FoZwJZUmE, Out The Chat https://claude.ai/artifact/AuEjqhBg2wKFuXEcQseakh. Source in `../sono/marketing/calendar/`.
- Account plan: one TikTok/Instagram per app with a distinct audience (Sono Bestie, Out The Chat), plus an optional studio account; this site is the "game library" that links them.
