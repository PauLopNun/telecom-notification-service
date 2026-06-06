# Suggested Commit Plan

This is the commit sequence I would follow when building the project in small
manual sessions. Each commit stays focused on one change and uses Conventional
Commits.

## Day 1

- `chore: init project structure`
- `chore: add python tooling configuration`
- `feat: add notification domain model`
- `test: add domain validation tests`

## Day 2

- `feat: add create notification use case`
- `test: add unit tests for create notification`
- `feat: add get notification use case`
- `fix: validate blank notification messages`

## Day 3

- `feat: add list notifications use case`
- `feat: add update notification status use case`
- `feat: add delete notification use case`
- `refactor: extract notification dto mapping`
- `test: add unit tests for notification use cases`

## Day 4

- `feat: add sqlalchemy notification model`
- `feat: add postgres repository implementation`
- `chore: add alembic migration setup`
- `test: add integration tests for notification repository`
- `fix: normalize postgres database urls for async driver`

## Day 5

- `feat: add fastapi notification routes`
- `fix: map domain errors to http responses`
- `test: add api tests for notification endpoints`
- `chore: add docker compose infrastructure`
- `docs: document local setup and api endpoints`

## Day 6

- `feat: add render deployment blueprint`
- `feat: add render self ping scheduler`
- `docs: add render and aws deployment notes`
- `chore: add github actions ci pipeline`
- `docs: complete architecture and roadmap sections`
