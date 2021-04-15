# ----
# base
# ----
FROM python:3.9 as base

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# -----
# build
# -----
FROM base as build

WORKDIR /build

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY ./pyproject.toml ./poetry.lock ./
COPY ./src/katubi ./katubi
RUN $HOME/.poetry/bin/poetry build --format wheel --no-interaction

# -----
# serve
# -----
FROM base as serve

WORKDIR /app
USER root

# Copy the build artifact and install.
COPY --from=build /build/dist /build/dist
RUN pip install /build/dist/*
RUN pip install gunicorn

# Add a script to allow running management commands.
COPY ./katubi-admin /usr/bin/katubi-admin
RUN chmod 755 /usr/bin/katubi-admin

# Collect static files.
RUN STATIC_ROOT=/srv/www/static katubi-admin collectstatic --no-input

# Create an app user.
RUN useradd --no-create-home --shell /bin/false app-user

USER app-user

# Add the Sentry release version to the environment.
ARG SENTRY_RELEASE
ENV SENTRY_RELEASE=$SENTRY_RELEASE

ENTRYPOINT ["gunicorn", "katubi.wsgi:application", "--bind", "0.0.0.0:8000"]
EXPOSE 8000
