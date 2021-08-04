# Self Hosted, self contained www.asciimation.co.nz/Blinkenlights ASCII Star Wars clone

![Docker Pulls](https://img.shields.io/docker/pulls/modem7/docker-starwars) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/modem7/docker-starwars/latest) [![Build Status](https://drone.modem7.com/api/badges/modem7/docker-starwars/status.svg)](https://drone.modem7.com/modem7/docker-starwars)

More info can be found here: www.asciimation.co.nz/Blinkenlights

# Configuration

```bash
version: "2.4"

services:

  starwars:
    image: modem7/docker-starwars
    container_name: StarWars
    ports:
      - 80:80
```
