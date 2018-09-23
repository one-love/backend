One Love REST API [![CircleCI](https://circleci.com/gh/one-love/backend.svg?style=svg)](https://circleci.com/gh/one-love/backend) [![Stories in Ready](https://badge.waffle.io/one-love/backend.png?label=ready&title=Ready)](https://waffle.io/one-love/backend) [![Coverage Status](https://coveralls.io/repos/github/one-love/backend/badge.svg?branch=master)](https://coveralls.io/github/one-love/backend?branch=master)
=================



This is the API part of [One Love](https://one-love.github.io) based on Python Flask.

### Contributing

If you are intresting in contributing to this project, be sure to visit the [contributing page](https://github.com/one-love/one-love/doc/contributing.md). For easier development, take a look at the [main One Love repository](https://github.com/one-love/one-love).

### Usage
To get a login token:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' http://onelove.vagrant:5000/api/v0/auth/tokens -X POST -d '{"email": "admin@example.com", "password": "Sekrit"}'



```
To use the token to get list of clusters:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: JWT <token>' http://onelove.vagrant:5000/api/v0/clusters
```

In the same way you can get other resorces/endpoints.


### Swagger
To use swagger open [Swagger UI](http://localhost:5000/api/v0/doc/)

