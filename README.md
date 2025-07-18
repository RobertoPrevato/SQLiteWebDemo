# SQLiteTest

Application to practice using volume mounts with Docker and Kubernetes.

This application uses a SQLite database to store fortune cookies, inside a
'/store/app.db' file. The application is built using the BlackSheep web framework
and SQLAlchemy ORM. When deployed to a container, the database file is stored
in a volume mount, so that it can be persisted across container restarts.

## Getting started

1. create a Python virtual environment
2. install dependencies
3. run the application

### For Linux and Mac

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python dev.py
```

### For Windows

```bash
py -3.13 -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python dev.py
```

### Env variables

To test serving the application at a different path prefix, set an env variable
`APP_ROUTE_PREFIX` with the desired prefix. This feature is available since
BlackSheep 2.1.0, and can be useful when using a proxy server and path based
routing.

```bash
APP_ROUTE_PREFIX="cookies" python dev.py
```

### Docker

Build an image using the example image.

```bash
docker build -t fortunecookies:0.0.1 .
```

Run the image once built, for example to map from the host `8080`:

```bash
docker run --rm -p 8080:80 fortunecookies
```

To use a mount for the database file, you can use the following command:

```bash
docker run --rm -p 8080:80 --name fortune -v ./store/:/home/store/ fortunecookies
```
