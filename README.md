# docker-starwars

Self hosted, self contained Docker image of the classic
[www.asciimation.co.nz/Blinkenlights](https://www.asciimation.co.nz/Blinkenlights)
ASCII Star Wars animation. I originally just grabbed the files straight off
the site and stuck them in a container — everything runs client-side in the
browser, nothing leaves the container, no ads, no analytics phoning home.
Which is more than you can say for the actual site.

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

Or Compose, if that's more your thing:

```yaml
services:
  starwars:
    image: modem7/docker-starwars
    container_name: starwars
    ports:
      - 8080:8080
```

Open `http://localhost:8080` and enjoy.

## What's actually in the image

- Content is entirely local — nothing gets fetched from `asciimation.co.nz`
  or anywhere else once it's running
- Built on `nginxinc/nginx-unprivileged`, runs as `uid 101`. No root, anywhere
- gzip on, plus the usual security headers (`X-Content-Type-Options`,
  `X-Frame-Options`, `Referrer-Policy`, `Content-Security-Policy`) — see
  `conf/nginx-site.conf` if you want the specifics
- `/healthz` backs the built-in `HEALTHCHECK`, so it actually means something
- Multi-arch: `amd64`, `arm/v6`, `arm/v7`, `arm64/v8`

## Keeping the animation content up to date

Upstream adds new scenes every so often, and I'm not going to remember to
go re-mirror the site by hand every time. So:

- **Manually**: `python3 scripts/update_film_data.py` — pulls whatever's
  current upstream and splices it in. Leaves the player code alone, and
  deliberately doesn't pull in upstream's ads/analytics or links to pages
  this image doesn't mirror.
- **On demand, from GitHub**: same thing, run as the *Update film data*
  workflow from the Actions tab. Opens a PR instead of pushing straight to
  `master`, so I get a chance to actually look at it first.
- **On a schedule**: *Check content freshness* runs weekly and opens a
  `content-freshness` issue the moment it's out of sync, so I don't have to
  remember to check either.

## Testing / CI

I don't trust "the image built" as proof that anything actually works, so
every push/PR touching the image builds it, boots a real container, and
pokes at it: page structure, gzip, the security headers, static assets,
non-root/no-sudo/no-world-writable-files, and a Playwright script that
checks the animation actually advances frames and that `Stop()`/`Play()`
etc. do what they say. See `.github/workflows/test.yml` if you want the
gory details.

`.woodpecker.yml` does the actual multi-arch build and Docker Hub push once
something's merged to `master`.

## Tags

| Tag | Description |
| :----: | --- |
| `latest` | Latest version |

## Credits

Not my work, I just packaged it up:

- [Simon Jansen](https://www.asciimation.co.nz) made the original asciimation.
- Notes from Mike Edwards, who wrote the player script this is based on:
  > Replacement telnet at asciimation.mirkwood.net:23/24. Port 23 is the
  > last released Star Wars asciimation by Simon Jansen, and port 24 is
  > Jansen's other goofy asciimation, The death of Jar Jar Binks.

## License

MIT, see [LICENCE.txt](LICENCE.txt).
