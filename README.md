# CMD Api

Do you want to expose a piece of shell as a Restful API without having to worry about looking for a complex or non-existent FaaS solution on your cloud provider? This is for you! 

This is the low cost FaaS that can be run wherever there is an OCI container runtime!

## Table of content

[[_TOC_]]
## Git repo

* Main repo: https://gitlab.comwork.io/oss/cmd-api
* Github mirror backup: https://github.com/idrissneumann/cmd-api

## Image on the dockerhub

The image is available and versioned here: https://hub.docker.com/r/comworkio/cmd-api

## How to use

You'll only have to configure this image as a pod if you're using Kubernetes or container if you're using something like docker, docker-compose, podman or whatever.

You'll find an example with docker-compose [here](./docker-compose.yml) and with Kubernetes [there](./deployment.yaml)
## What's available

This image will provide you the following commands:
* python3
* bash
* curl
* jq
* yq
* kubectl

N.B:

* If there is something that miss, feel free to write your own Dockerfile that inherit this image (`comworkio/cmd-api`).
* If you think that there is too much stuffs in this images, feel free to pick only what you need with a multistage build!

### Environment variables

* `FLASK_RUN_HOST`: api address (default binded to `0.0.0.0`, shouldn't change on a Kubernetes context)
* `FLASK_RUN_PORT`: api port (default binded to `8080`)
* `API_CMD`: the command to run when you call the endpoints
* `MANIFEST_FILE_PATH`: the manifest file path (a file that you can override to provide apps information like the version built etc)

### The endpoints

* `/` or `/health`: healthcheck endpoint
* `/cmd` or `/cmd-api`: synchronous execution of the command (you'll get the output in the http response body)
* `/cmd/async` or `/cmd-api/async`: asynchronous execution of the command (you won't get the output in the http response body)
* `/manifest`: get the manifest informations

See the test with docker part to get more details about those endpoints.

## Test with docker

```shell
$ docker-compose up
$ curl localhost:8080
{"alive": true}
$ curl localhost:8080/cmd
{"executed": true, "details": "total 76\ndrwxr-xr-x   2 root root 4096 Dec 12 20:43 __pycache__\n-rw-r--r--"}
$ curl -X POST localhost:8080/cmd -d '{"argv": "-a"}'
{"executed": true, "details": "total 76\ndrwxr-xr-x   2 root root 4096 Dec 12 20:43 __pycache__\n-rw-r--r--"}
$ curl localhost:8080/cmd/async
{"executed": true, "async": true}
$ curl -X POST localhost:8080/cmd/async -d '{"argv": "-a"}'
{"executed": true, "async": true}
$ curl localhost:8080/manifest 
{"version": "2.1", "sha": "1c7cb1f"}
```
