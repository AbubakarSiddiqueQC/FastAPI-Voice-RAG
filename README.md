## Setup virtual environment

```sh
python -m venv .venv
## for mac/linux
source .venv/bin/activate
## for windowa
.venv/bin/activate

```

## Install requirements

```sh
pip install -r requirements.txt
```

## Setup environment
1. cp `.env.sample` `.env`
2. Include `DATABASE_URL`
   ```
   DATABASE_URL="postgresql://<user>:<password>@<url>:5432/postgres?schema=<scheme>"
   ```


## Generate Prisma Client and Nexus

```sh
prisma generate
```

## Start server

```sh
uvicorn main:app --reload
```

## Notes

> After installing packages

```sh
pip freeze > requirements.txt
```
