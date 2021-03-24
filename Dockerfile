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

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./
COPY ./src/katubi ./katubi
RUN poetry build --format wheel --no-interaction

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

# Create an app user.
RUN useradd --no-create-home --shell /bin/false app-user

USER app-user
ENTRYPOINT ["gunicorn", "katubi.wsgi:application", "--bind", "0.0.0.0:8000"]
EXPOSE 8000
