# docker-starwars

Self-hosted, self-contained Docker image of the classic
[www.asciimation.co.nz/Blinkenlights](https://www.asciimation.co.nz/Blinkenlights)
ASCII Star Wars animation — the whole thing runs client-side in the
browser, no external requests, no ads, no analytics.

[![status-badge](https://woodpecker.modem7.com/api/badges/4/status.svg?events=push%2Cmanual)](https://woodpecker.modem7.com/repos/4)
[![Test](https://github.com/modem7/docker-starwars/actions/workflows/test.yml/badge.svg)](https://github.com/modem7/docker-starwars/actions/workflows/test.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/modem7/docker-starwars)](https://hub.docker.com/r/modem7/docker-starwars)
[![Docker Image Size (tag)](https://img.shields.io/docker/image-size/modem7/docker-starwars/latest)](https://hub.docker.com/r/modem7/docker-starwars)
[![GitHub last commit](https://img.shields.io/github/last-commit/modem7/docker-starwars)](https://github.com/modem7/docker-starwars/commits/master)
[![License: MIT](https://img.shields.io/github/license/modem7/docker-starwars)](LICENCE.txt)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/modem7)

## Screenshot

![image](https://user-images.githubusercontent.com/4349962/128192966-26c74fd7-839c-49ce-b00f-af1050aece90.png)

## Quick start

```bash
docker run -d --name starwars -p 8080:8080 modem7/docker-starwars
```

Or with Compose:

```yaml
services:
  starwars:
    image: modem7/docker-starwars
    container_name: starwars
    ports:
      - 8080:8080
```

Then open `http://localhost:8080`.

## What's in the image

- Content is entirely local to the container — nothing is fetched from
  `asciimation.co.nz` (or anywhere else) at runtime
- Built on `nginxinc/nginx-unprivileged`, runs as an unprivileged user
  (`uid 101`), no root anywhere in the chain
- gzip compression and baseline security headers
  (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
  `Content-Security-Policy`) configured in `conf/nginx-site.conf`
- A `/healthz` endpoint backs the image's built-in `HEALTHCHECK`
- Multi-arch: `linux/amd64`, `linux/arm/v6`, `linux/arm/v7`, `linux/arm64/v8`

## Keeping the animation content up to date

The embedded animation data (`src/index.html`'s `film` array) is mirrored
from the upstream site rather than hand-maintained, since upstream adds new
scenes from time to time. Three ways to keep it in sync:

- **Manually**: `python3 scripts/update_film_data.py` — fetches the current
  content from upstream and splices it in, leaving the player's own code
  and everything intentionally excluded (upstream's ads, analytics, and
  links to pages this image doesn't mirror) untouched.
- **On demand from GitHub**: run the *Update film data* workflow from the
  Actions tab — does the same thing, then opens a PR with the diff instead
  of pushing straight to `master`.
- **Automatically checked weekly**: the *Check content freshness* workflow
  runs `scripts/check_film_freshness.py` on a schedule and opens a
  `content-freshness`-labeled issue the first time it detects drift.

## Testing / CI

Every push/PR that touches the image (`Dockerfile`, `src/**`,
`conf/nginx-site.conf`) builds the image, boots a real container, and
asserts on its actual behavior rather than just that it builds: page
structure, gzip, security headers, static asset serving, non-root/no-sudo/
no-world-writable-files, and a Playwright script confirming the animation
actually advances frames and that the transport controls (`Stop()`,
`Play()`, etc.) work. See `.github/workflows/test.yml`.

`.woodpecker.yml` handles the actual multi-arch build and Docker Hub push
on a successful merge to `master`.

## Tags

| Tag | Description |
| :----: | --- |
| `latest` | Latest version |

## Credits

- [Simon Jansen](https://www.asciimation.co.nz) created the original
  asciimation.
- Notes from Mike Edwards, author of the player script this is based on:
  > Replacement telnet at asciimation.mirkwood.net:23/24. Port 23 is the
  > last released Star Wars asciimation by Simon Jansen, and port 24 is
  > Jansen's other goofy asciimation, The death of Jar Jar Binks.

## License

[MIT](LICENCE.txt)
