# CMD Api

An api that take a command into an environment variable and execute this commande with a restful/http endpoint.

This is usefull to execute some command inside Kubernetes pods without having to override your application image.

## Git repo

* Main repo: https://gitlab.comwork.io/oss/cmd-api
* Github mirror backup: https://github.com/idrissneumann/cmd-api

## Environment variables

* `FLASK_RUN_HOST`: api address (default binded to `0.0.0.0`, shouldn't change on a Kubernetes context)
* `FLASK_RUN_PORT`: api port (default binded to `8080`)
* `API_CMD`: the command to run when you call the `/cmd` endpoint

## The endpoints

* `/`: healthcheck
* `/cmd`: synchronous execution of the command (you'll get the output in the http response body)

## Testing with docker

```shell
$ docker-compose up
$ curl localhost:8080
{"alive": true}
$ curl localhost:8080/cmd
{"executed": true, "details": "total 76\ndrwxr-xr-x   2 root root 4096 Dec 12 20:43 __pycache__\n-rw-r--r--"}
```
