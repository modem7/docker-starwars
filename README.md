# Self Hosted, self contained www.asciimation.co.nz/Blinkenlights ASCII Star Wars clone

![Docker Pulls](https://img.shields.io/docker/pulls/modem7/docker-starwars) ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/modem7/docker-starwars/latest) [![Build Status](https://drone.modem7.com/api/badges/modem7/docker-starwars/status.svg)](https://drone.modem7.com/modem7/docker-starwars)
[![GitHub last commit](https://img.shields.io/github/last-commit/modem7/docker-starwars)](https://github.com/modem7/docker-starwars)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/modem7)

More info can be found here: www.asciimation.co.nz/Blinkenlights

Further notes from Mike Edwards, the author of the player script towel used: Replacement telnet at asciimation.mirkwood.net:23/24. Port 23 is the last released Star Wars asciimation by Simon Jensen, and port 24 is Jansen's other goofy asciimation, The death of Jar Jar Binks. 

Image is based on nginxinc/nginx-unprivileged, and all the content is local to the container.

# Container Screenshot
![image](https://user-images.githubusercontent.com/4349962/128192966-26c74fd7-839c-49ce-b00f-af1050aece90.png)


# Breaking change
Due to changing the image to nginxinc/nginx-unprivileged, the ports have changed from `80` to `8080`. 
Please update your files accordingly. 

# Configuration

```bash
version: "2.4"

services:

  starwars:
    image: modem7/docker-starwars
    container_name: StarWars
    ports:
      - 8080:8080
```

# Tags
| Tag | Description |
| :----: | --- |
| Latest | Latest version |
