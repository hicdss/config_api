# config_api

Config_api is a simple microservice that serves as a single-source-of-truth about various elements of your infrastructure and environments. For example it can be used as port mapping configuration of docker containers, filesystem paths, volume names, network interfaces etc. etc. It is useful as a central source-of-truth in distributed CI/CD systems. Imagine you have legacy `docker-compose` development environment, where many docker containers run on a single host. You can create a simple Python dictionary and pass it to `config_api` to retrieve data, eg. listening ports or database connection strings in a deployment pipeline, eg:

```
export environment=dev
export webapp_app_port=$(curl https://you-config-api.domain.internal/config-api/webapp/${environment}/app_port -s)
docker run -d -p "${webapp_port}:80" webapp:latest
```

See below for sample configuration.

## Preparation

Use `FROM` directive in your `Dockerfile` toghether with `environment_config.py` file. Directory layout is simple and as follows:


```
my_config_api/
├── Dockerfile
└── environment_config.py
```

### `Dockerfile`

```dockerfile
FROM hicrondss/config_api:latest
COPY environment_config.py /app/config_api/model/environment_config.py
```

### `envrionment_config.py`

This file should be a valid python file with `ENVIRONMENTS` variable defined as dictionary. Eg.:


```python
ENVIRONMENTS = {
    'webapp' : {
        'staging' : {
            'docker_app_port': 8181,
            'docker_sql_port': 3307,
        },
        'dev' : {
            'docker_app_port': 8080,
            'docker_sql_port': 3306,
        },
    }
}

```

### Build & deploy

With those two files you can now build your docker image:

```bash
docker build -t my_config_api:latest .
docker run -d -p 8888:8888 my_config_api:latest
```

Or use `docker-compose.yml`:

```yml
version: "3.3"
services:
    my_config_api:
        build:
            context: .
        ports:
            - 8888:8888
```

### Environment variables

By default application listens internally on port 8888, but this can be changed with `PORT` environment variable.

Also you can setup a custom root URL path, so instead of `/config-api` you can have whatever you want, by setting `ROOT_RESOURCE_NAME` variable using dockerfile directive `ENV`.

```dockerfile
FROM hicrondss/config_api:latest
COPY environment_config.py /app/config_api/model/environment_config.py
ENV PORT=7777
ENV ROOT_RESOURCE_NAME=awesome-api
```

# Usage

After you start the container you will be able to make http requests to retrieve your configuration. Using `envrionment_config.py` from above you could do:

```bash
curl -s http://localhost:8888/config-api/webapp/staging/docker_app_port
```

which would output:

    8181

You can use it in your Jenkins pipelines or `build.gradle` file.

# Best practices

## Security

Always keep your config_api behind a reverse proxy and protect it.

## Basic auth

Use htpasswd utility to create hashed password:

```bash
sudo apt-get update
sudo apt-get install apache2-utils

htpasswd -c /etc/apache2/.config_api_htpasswd config_api_user
```

Example configuration for Apache 2.4 would be:

```conf
    <Location /config-api/>
        AuthType Basic
        AuthName "Authentication Required"
        AuthUserFile "/etc/apache2/.config_api_htpasswd"
        Require valid-user

        ProxyPass http://localhost:8888/config-api/
        ProxyPassReverse http://localhost:8888/config-api/

        Header unset Server # remove printing "meinheld/1.0.1" in "Server" response header
    </Location>
```

# Development

```bash
make build # builds docker image
make test_in_docker # runs Python linters
make run # starts container on 8888 port
make down # remove the container
make logs # see logs
```
