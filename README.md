# FastAPI Posts API

REST API for posts with user authentication and voting, built with FastAPI and PostgreSQL.

**Live demo:** https://desktop-tutorial-lgnj.onrender.com/docs
(Free hosting: the first request after idle can take about a minute.)

## Tech stack
FastAPI, SQLAlchemy, Alembic, PostgreSQL, uv, Render

## Features
- User registration and login (OAuth2 + JWT)
- CRUD for posts(can create users, authorization required for each post made by a user)
- Since its only a test, a user can stay logged in for 60 mins after logging in; authorization required again afterwards.
- Voting on posts

## Run locally
```bash
git clone https://github.com/zxamin26/fastapi-apis.git
cd REPO
uv sync
copy .env.example .env        # then fill in your values
uv run alembic upgrade head
uv run fastapi dev app/backend.py
```
Open http://127.0.0.1:8000/docs

## Environment variables
| Name | Purpose |
|------|---------|
| SQLALCHEMY_DATABASE_URL | Database connection URL |
| SECRET_KEY | Used to sign login tokens |

## Status
Working: auth, posts, votes, migrations, deployed.
Next: tests, Docker, CI.