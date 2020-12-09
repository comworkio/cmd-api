# CMD Api

An api that take a command into an environment variable and execute this commande with a restful/http endpoint.

This is usefull to execute some command inside Kubernetes pods without having to override your application image.

You'll just need to add a container with this image to your pod and enable this :

```yaml
shareProcessNamespace: true
```
