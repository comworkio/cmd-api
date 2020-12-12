# CMD Api

Make a shell command available as Restful api.

## Git repo

* Main repo: https://gitlab.comwork.io/oss/cmd-api
* Github mirror backup: https://github.com/idrissneumann/cmd-api

## Environment variables

* `FLASK_RUN_HOST`: api address (default binded to `0.0.0.0`, shouldn't change on a Kubernetes context)
* `FLASK_RUN_PORT`: api port (default binded to `8080`)
* `API_CMD`: the command to run when you call the endpoints

## The endpoints

* `/` or `/health`: healthcheck endpoint
* `/cmd` or `/cmd-api`: synchronous execution of the command (you'll get the output in the http response body)
* `/cmd/async` or `/cmd-api/async`: asynchronous execution of the command (you won't get the output in the http response body)

## Test with docker

```shell
$ docker-compose up
$ curl localhost:8080
{"alive": true}
$ curl localhost:8080/cmd
{"executed": true, "details": "total 76\ndrwxr-xr-x   2 root root 4096 Dec 12 20:43 __pycache__\n-rw-r--r--"}
$ curl localhost:8080/cmd/async
{"executed": true, "async": true}
```
