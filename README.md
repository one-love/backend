One Love REST API
=================

This is Flask based API part of [One Love](https://one-love.github.io/) project.

### Contributing to One Love
We will happily accept pull requests that conform to our [Contributing guidelines](CONTRIBUTING.md). For easier development, take a look at [One Love Vagrant repository](https://github.com/one-love/vagrant-one-love)

### Usage
To get a login token:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' https://192.168.33.33/auth -X POST -d '{"username": "admin@example.com", "password": "Sekrit"}'
```

To use the token to get list of clusters:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <token>' http://192.168.33.33:5000/api/v0/clusters
```

In the same way you can get other resorces/endpoints

### Swagger
To use swagger open [Swagger UI](https://192.168.33.33/)
