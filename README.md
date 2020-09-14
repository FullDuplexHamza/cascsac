# This is a repo for testing Drone CI (on NixOS)
On this repo i was working to setup succesfully the continous integration on my home server. Small tutorial above...

## Tutorial for Traefik + NixOS environment
1. Github configuration. Follow the OAuth configuration on [this tutorial](https://rubynor.com/blog/2020/06/setting-up-drone-ci-for-rails-apps/)
   
2. Traefik things. Fill a docker-compose file.For example, like this: 
```
version: '3.7'

services:
  drone-server:
    container_name: drone-server
    image: drone/drone
    restart: unless-stopped
    ports:
      - 8080:80
    volumes:
      - /var/lib/drone:/data
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DRONE_GITHUB_SERVER=https://github.com
      - DRONE_GITHUB_CLIENT_ID=<GITHUB_ID>
      - DRONE_GITHUB_CLIENT_SECRET=<GITHUB_SECRET>
      - DRONE_AGENTS_ENABLED=true
      - DRONE_RPC_SECRET=<Your RPC_SECRET>
      - DRONE_SERVER_HOST=<Your URL>
      - DRONE_SERVER_PROTO=https
      - DRONE_TLS_AUTOCERT=true
      - DRONE_USER_CREATE=username:<Username GITHUB>,admin:true
      - DRONE_LOGS_TRACE=true
      - DRONE_LOGS_PRETTY=true
      - DRONE_LOGS_COLOR=true
    labels:
      - traefik.enable=true
      - traefik.http.services.drone.loadbalancer.server.port=80
      - traefik.http.routers.drone.entryPoints=web-secure
      - traefik.http.routers.drone.rule=Host(`<Your URL>`)
      - traefik.http.routers.drone.tls.certresolver=default
```

Start the container:
 `docker-compose up -d`  

3. Setting up the executor. In this case, I need a host runner executor. Actually I'm using NixOS, so:
   1. Download the drone-exec binary (its on official website)
`curl -L https://github.com/drone-runners/drone-runner-exec/releases/latest/download/drone_runner_exec_linux_amd64.tar.gz | tar zx`
   2. Move to `/root/bin/`
   3. Add to configuration.nix:
```
environment.etc.drone-runner-exec = {
    target = "drone-runner-exec/config";
    text = ''
    DRONE_RPC_PROTO=https
    DRONE_RPC_HOST=<Your host URL>
    DRONE_RPC_SECRET=<Your RPC_SECRET>
    DRONE_UI_USERNAME=root
    DRONE_UI_PASSWORD=root
    '';
  };

  systemd.services.drone-runner-exec = {
    description = "Drone Exec Runner";
    startLimitIntervalSec = 5;
    serviceConfig = {
      ExecStart = "/root/bin/drone-runner-exec service run --config /etc/drone-runner-exec/config";
    };
    wantedBy = [ "multi-user.target" ];
    path = [ pkgs.git pkgs.docker pkgs.docker-compose ];
  };
  ```
  4. Go to ur Drone URL and auth with ur GitHub account. 
  5. Enable a repo to be CI and add a `.drone.yml` like this:
```
kind: pipeline
type: exec
name: default

platform:
  os: linux
  arch: amd64

steps:
- name: build
  commands:
    - docker build -t drone-tests .

- name: run
  commands:
    - cd /var/docker/project
    - docker-compose stop drone-tests
    - docker-compose up -d drone-tests
```
6. You can check the deploy status on Drone webpage.

## Sources:
* https://ansonvandoren.com/posts/ci-cd-with-drone/
* https://rubynor.com/blog/2020/06/setting-up-drone-ci-for-rails-apps/
* https://gist.github.com/anson-vandoren/d1abca7d5bf56d957e86bca93639ca2c
* https://docs.drone.io/server/provider/github/
* https://dev.to/fuksito/private-ci-using-private-docker-registry-with-drone-io-almost-free-15ek
* https://medium.com/faun/setup-a-drone-cicd-environment-on-docker-with-letsencrypt-69b259d398fb
* https://discourse.drone.io/t/running-drone-via-traefik/3715/5