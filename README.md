# CMD Api

An api that take a command into an environment variable and execute this commande with a restful/http endpoint.

This is usefull to execute some command inside Kubernetes pods without having to override your application image.

You'll just need to add a container with this image to your pod and enable this :

```yaml
shareProcessNamespace: true
```

## Environment variables

* `FLASK_RUN_HOST`: api address (default binded to `0.0.0.0`, shouldn't change on a Kubernetes context)
* `FLASK_RUN_PORT`: api port (default binded to `8080`)
* `API_CMD`: the command to run when you call the `/` endpoint

## Git repo

* Main repo: https://gitlab.comwork.io/oss/cmd-api
* Github mirror backup: https://github.com/idrissneumann/cmd-api
