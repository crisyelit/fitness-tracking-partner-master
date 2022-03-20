# Fitness tracking partner

## Environment

To start the application it is necessary to include the .env file

## Build

```shell
docker compose build
```

## Running the application

The application is built with Django and already has all environment configured with docker. To start the application you will need `docker` and `docker compose` installed on the machine. Having that you may run:

```shell
docker compose up
```

And then the application and database will be started:

```shell
Starting app_mailhog_1 ... done
Starting app_db        ... done
Starting app_redis     ... done
Starting app_celery      ... done
Starting app_celery_beat ... done
Starting app_web     ... done
```

The application will be avaible on _PORT 8000_ by default, but it's configurable via `docker-compose.yml` file as an environment variable.


## Running makemigrations

```shell
docker exec -ti app_web python /code/manage.py makemigrations
```

## Running empty makemigrations

```shell
docker exec -ti app_web python /code/manage.py makemigrations app_name --empty
```

## Running the migrations

```shell
docker exec -ti app_web python /code/manage.py migrate
```

## Create super user

```shell
docker exec -ti app_web python /code/manage.py createsuperuser
```

## Create translations

```shell
docker exec -ti fitness_tracking_partner_web django-admin makemessages -l en --ignore apps

```

## Create compile messages

```shell
docker exec -ti fitness_tracking_partner_web django-admin compilemessages --ignore apps

```

# fitness-tracking-partner-master
