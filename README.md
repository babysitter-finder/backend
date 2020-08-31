# Babysitter Finder ![Status badge](https://img.shields.io/badge/status-in%20progress-yellow)


Babysitter finder is a project that offers you the babysitter service, through science and astheroids study.

## 📢 Requirements
- docker
- docker-compose

## 🛠 Instalation
1. Clone this project.

2. Change of directory to the root of the project.
```bash
  cd hisitter
```
3. Build the images.
```bash
  docker-compose -f production.yml build
```
4. Run the migrations to create the tables in the database.
```bash
   docker-compose -f production.yml run --rm django python manage.py makemigrations
   docker-compose -f production.yml run --rm django python manage.py migrate
```
5. Run it in production
```bash
  docker-compose -f production.yml up -d
```

## Debugging
1. In the root of project.
```bash
docker-compose -f local.yml build
```
2. After construction run the containers.
```bash
    docker-compose -f local.yml up
```
3. If you want run the migrations.
```bash
   docker-compose -f local.yml run --rm django python manage.py makemigrations
   docker-compose -f local.yml run --rm django python manage.py migrate
```

## 🔧 Built with
- [Django](https://www.djangoproject.com/) (django, django-celery-beat, django-redis, django-mailgun)
- [Django REST FRAMEWORK](https://www.django-rest-framework.org/)
- [Traefik] (https://docs.traefik.io/)
- [Redis](https://redis.io/)
- [Postgres](https://www.postgresql.org/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [AWS EC2](https://aws.amazon.com/es/ec2/)
- [MAILGUN] (https://www.mailgun.com/)
- [SENTRY] (https://sentry.io/)

## 🚀 Deploy
1. Configure a AWS EC2 machine and install docker, copy your project in the machine
```bash
  scp -i SecureKey.pem /path/hisitter ubuntu@<ippublic>:.
```
2. After run the project in production you need set in a dot env file, called .production the next:

| KEY                      | VALUE                             |
|--------------------------|-----------------------------------|
| DJANGO_READ_DOT_ENV_FILE | TRUE                              |
| DJANGO_SETTINGS_MODULE   | config.settings.production        |
| DJANGO_SECRET_KEY        | Secure Key                        |
| DJANGO_SERVER_EMAIL      | hisitter<noreply@hisitter.xyz>    |
| MAILGUN_API_KEY          | Secure Key                        |
| MAILGUN_DOMAIN           | mail.hisitter.xyz                 |
| DJANGO_AWS_STORAGE       | Define in AWS                     |
| SENTRY_DSN               | Obtain this in https://sentry.io/ |
| REDIS_URL                | redis://redis:6379/0              |
| CELERY_FLOWER_USER       | Secure key                        |
| CELERY_FLOWER_PASSWORD   | Secure key                        |

3. Build and run the containers:
```bash
    docker-compose -f production.yml build
    docker-compose -f production.yml up -d
```
4. You can install supervisor in ubuntu to avoid the fallen in the containers.

## 🗄️ Backend Implementations

- **[API Babysitter Finder][backend_project]**

##  Contributors

The staff:

- **[Abdiel Ortega][abdiel_github]** _(Frontend Developer and Interface designer)_
- **[Angel Estrada][angel_github]** _(Interface designer)_

This project exists thanks to  [Platzi](https://platzi.com/).

<img src="https://www.morelosinnovador.org/images/logo_platzi.jpg" width="150" />
.

## 📜 License
The MIT License (MIT)

## 🖌️ Design System

The design system and the rest of the documentation can be found in [Notion](https://www.notion.so/Kanban-f4ed2788eaf8473a912444755a0d1d02) and the design can be found at [Figma](https://www.figma.com/file/SJbT26D4huBkATw97d8heG/finder)

## 🙏 Acknowledgment
* To Coach Ana Belisa Martinez.
* To Platzi Staff.

[angel_github]: https://github.com/ricardoares1989
[abdiel_github]: https://github.com/abdieljortega
[backend_project]: https://github.com/babysitter-finder/backend
[frontend_project]: https://github.com/babysitter-finder/frontend



