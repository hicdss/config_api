# config_api

Config_api is a simple microservice that serves as a single-source-of-truth about various elements of your infrastructure and environments. For example it can be used as port mapping configuration of docker containers, filesystem paths, volume names, network interfaces etc. etc.

## API endpoints

`/config-api/all` - returns full configuration
`/config-api/list` - returns list of apps
`/config-api/<app_name>` - return app config
`/config-api/<app_name>/<env>` - return environment config for a given app
`/config-api/<app_name>/<env>/<parameter>` - return a parameter

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
    'webapp' : {  ## APPLICATION LEVEL
        'staging' : {  ## ENVIRONMENT LEVEL
            'docker_app_port': 8181, ## PARAMETER LEVEL
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
docker run -d -p 8080:8080 my_config_api:latest
```

Or use `docker-compose.yml`:

```yml
version: "3.3"
services:
	my_config_api:
		build:
			context: .
		ports:
			- 8080:8080
```

# Usage

After you start the container you will be able to make http requests to retrieve your configuration. Using `envrionment_config.py` from above you could do:

```bash
curl -s http://localhost:8080/config-api/webapp/staging/docker_app_port 
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

        ProxyPass http://localhost:8080/config-api/
        ProxyPassReverse http://localhost:8080/config-api/
    </Location>
```

# Development

```bash
make build && make run
```