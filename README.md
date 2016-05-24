One Love REST API
=================

[![Run Status](https://api.shippable.com/projects/5478a4b2d46935d5fbbee379/badge?branch=master)](https://app.shippable.com/projects/5478a4b2d46935d5fbbee379)
[![Stories in Ready](https://badge.waffle.io/one-love/backend.png?label=ready&title=Ready)](https://waffle.io/one-love/backend)

This is Flask based API part of [One Love](https://one-love.github.io/) project.

### Contributing to One Love
We will happily accept pull requests that conform to our [Contributing guidelines](CONTRIBUTING.md). For easier development, take a look at [One Love Vagrant repository](https://github.com/one-love/vagrant-one-love)

### Usage
To get a login token:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' http://onelove.vagrant:5000/api/v0/auth/tokens -X POST -d '{"email": "admin@example.com", "password": "Sekrit"}'



```

### Testing
In order to run a test. Run the following command in the repo directory.

    $ docker-compose run --rm backend bin/test.sh

When the testing is finished you can get one of the following results:

  - . test passed
  - F your test failed
  - E something really bad happend



To use the token to get list of clusters:
```bash
curl -k -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: JWT <token>' http://onelove.vagrant:5000/api/v0/clusters
```

In the same way you can get other resorces/endpoints

### Swagger
To use swagger open [Swagger UI](http://onelove.vagrant:5000/api/v0/doc/)
