FROM python:3.9-slim AS base

## Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# fault handler on
ENV PYTHONFAULTHANDLER 1

# Install Dependencies
FROM base AS python-dependencies

### Install pipenv
RUN pip install pipenv

### Install dependencies in /.venv
COPY test_client/Pipfile .
COPY test_client/Pipfile.lock .

# Install pipenv packages to the project dir
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# Our runtime should be minimal so we use distroless
FROM gcr.io/distroless/python3

WORKDIR /app

# Copy the python dependencies as distroless is minimal 
COPY --from=python-dependencies /.venv/lib/python3.9/site-packages /app/site-packages

# Set Python path
ENV PYTHONPATH /app/site-packages
COPY . .

EXPOSE 8000
ENTRYPOINT ["python", "test_client/app.py"]
