# Assignment 02: CI/CD Pipeline Setup and Demonstration

## Purpose

This project is a practical example of how to set up a Continuous Integration (CI) and Continuous Deployment (CD) pipeline for a small Flask API.

The assignment requires you to:

1. Fork the provided repository into your own GitHub account.
2. Make a meaningful change to the application.
3. Configure CI so tests run automatically on every commit.
4. Configure CD so the application is deployed to a staging environment only after CI passes.
5. Document the work with links, screenshots, and explanations.

Repository used for this assignment:

- https://github.com/edonosotti/ci-cd-tutorial-sample-app

Current fork used for this work:

- https://github.com/anjananadee23/ci-cd-tutorial-sample-app

---

## What This Repo Contains

This application is a small Flask REST API with:

- `GET /` returning a JSON status message
- `GET /menu` returning the special of the day if a menu row exists
- `GET /health` returning a simple health check response

It also includes:

- database models and migrations
- a seed script that inserts sample data
- unit tests using `unittest`
- GitHub Actions workflows for CI and CD
- Docker support for containerized deployment

---

## Assignment Requirements and How to Complete Them

### Step 1: Fork, Clone, and Commit

#### What to do

1. Fork the repository to your own GitHub account.
2. Clone your fork to your local machine.
3. Make a meaningful change.
4. Commit and push the change to your fork.

#### What counts as a meaningful change

Examples:

- change response text on an endpoint
- add a new endpoint
- extend a unit test
- add validation or small feature behavior

#### What was done in this repo

- Added a new `GET /health` endpoint in `app/routes.py`.
- Updated the home endpoint response text.
- Added a unit test for `/health` in `tests/test_routes.py`.

#### Good commit practice

Use a clear commit message, for example:

```sh
git commit -m "Add health endpoint and CI/CD workflow"
```

---

### Step 2: Configure Continuous Integration (CI)

#### Goal

CI must automatically:

- run on each commit or pull request
- install dependencies
- run the test suite
- show clear pass/fail feedback

#### Tool chosen

GitHub Actions.

#### CI workflow used in this repo

File:

- `.github/workflows/ci.yml`

What it does:

- triggers on pushes to `main`, `master`, and `staging`
- triggers on pull requests to `main` and `master`
- sets up Python 3.12
- installs dependencies from `requirements.txt`
- runs database migrations using SQLite
- runs `python -m unittest discover -v`

#### Why this is a good CI setup

- It runs automatically.
- It checks the project the same way every time.
- It provides visible pass/fail output in GitHub Actions.

#### How to verify CI manually

After pushing to GitHub:

1. Open your repository.
2. Click the `Actions` tab.
3. Open the latest `CI` run.
4. Confirm the job is green and all test steps pass.

#### Optional improvements

If you want a stronger CI pipeline, you can add:

- a Python version matrix
- coverage reporting
- linting with `flake8` or `ruff`
- caching for pip dependencies

---

### Step 3: Configure Continuous Delivery (CD)

#### Goal

CD must deploy the app to a staging environment only if CI passes.

The staging environment must be:

- separate branch deployment, or
- different hosting service/server, or
- containerized environment hosted separately

It must be reachable by a URL.

#### Tool chosen

GitHub Actions + Docker + Render.

#### CD workflow used in this repo

File:

- `.github/workflows/cd-render.yml`

What it does:

- triggers after the CI workflow completes successfully on the `staging` branch
- deploys only after CI tests pass
- uses the repo's Dockerfile as the container build source for the staging service
- calls the Render deploy API

#### Existing Docker image workflow in this repo

File:

- `.github/workflows/docker_build_push.yml`

What it does:

- runs tests and linting before image publishing
- builds and pushes a Docker image when a release is published
- uses the repository's Dockerfile as the image source

This file is useful if you want to demonstrate a full container workflow in addition to staging deployment.

#### Required secrets

You must add these repository secrets in GitHub:

- `RENDER_SERVICE_ID`
- `RENDER_API_KEY`

If these secrets are not configured yet, the CD workflow will stop with a clear error because the deployment cannot happen without a real Render service and API key.

#### How to add the secrets

1. Open the repository on GitHub.
2. Go to `Settings`.
3. Open `Secrets and variables`.
4. Select `Actions`.
5. Add the two secrets above.

#### How the staging deployment works

1. Merge or push changes to the `staging` branch.
2. GitHub Actions runs the CI workflow and executes the tests.
3. If CI passes, the CD workflow starts automatically.
4. GitHub Actions sends a deploy request to Render.
5. Render rebuilds or redeploys the Docker container from the repository's `Dockerfile`.
6. The staging app becomes available at the Render URL.

#### Why the trigger order matters

The repository now uses a `workflow_run` trigger for CD, so deployment happens after CI finishes successfully instead of running in parallel with the test job. This is the correct CI-then-CD sequence for the assignment.

#### Why Docker is the better staging choice for this repo

- The repository already includes a `Dockerfile`.
- Docker keeps the staging environment close to production.
- Docker lets you package the app, dependencies, and startup command together.
- It satisfies the assignment's requirement for a containerized staging environment.
- The container now runs database migrations and seeds data before starting the app, so the staging site is usable after deployment.

#### Important note about deployment

The repository can now express the correct CI -> CD order, but the Render staging app still needs to be created in your Render account and connected through these secrets:

- `RENDER_SERVICE_ID`
- `RENDER_API_KEY`

Without those values, the CD workflow cannot actually deploy the container.

#### Why this satisfies the assignment

- The app is running in a separate staging environment.
- The deployment is controlled by the pipeline.
- Deployment happens only after tests succeed.
- The staging service is accessible through a URL.

---

## Local Setup and Run Instructions

### 1. Create and activate a virtual environment

```sh
python -m venv .venv
```

PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run database migrations

Set the Flask app first:

```powershell
$env:FLASK_APP='bootstrap.py'
```

Then run:

```sh
python -m flask db upgrade
```

### 4. Seed the database

```sh
python seed.py
```

### 5. Run the tests

```sh
python -m unittest discover -v
```

### 6. Run the app locally

```sh
python -m flask run
```

Open:

- http://127.0.0.1:5000/
- http://127.0.0.1:5000/health
- http://127.0.0.1:5000/menu

---

## Docker Option

This repo includes a `Dockerfile`, and Docker is the preferred staging environment for this assignment because it matches the containerized deployment option.

Build the image:

```sh
docker build -t ci-cd-tutorial-sample-app:latest .
```

Run the container:

```sh
docker run -d -p 8000:8000 ci-cd-tutorial-sample-app:latest
```

Open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/menu

### Docker notes for assignment submission

- Use Docker as the staging environment if you want the simplest container-based deployment story.
- In your report, describe the staging environment as a Docker container hosted on Render or another server.
- Include a screenshot of the running app in the browser and a screenshot of the successful deployment workflow.

This is useful if you want your staging environment to be container-based.

### Docker submission checklist

- mention the `Dockerfile` in the report
- mention that CI validates the code before deployment
- mention that CD redeploys the container only after tests pass
- include the staging URL from Render or your chosen host
- include screenshots of the Docker-based deploy and the running app

---

## Files That Matter for the Assignment

- `app/routes.py` - application endpoints
- `tests/test_routes.py` - unit tests
- `seed.py` - database seed data
- `requirements.txt` - Python dependencies
- `.github/workflows/ci.yml` - CI pipeline
- `.github/workflows/cd-render.yml` - CD pipeline
- `Dockerfile` - container deployment option
- `README.md` - original project notes

---

## How the Current Implementation Maps to the Assignment

### Step 1 mapping

- Forked the repo
- Cloned locally
- Made a meaningful change by adding `/health`
- Updated tests
- Committed and pushed changes

### Step 2 mapping

- CI is implemented with GitHub Actions
- It triggers on push and pull request events
- It installs dependencies
- It runs migrations and unit tests
- Pass/fail is visible in GitHub Actions

### Step 3 mapping

- CD is implemented with GitHub Actions and Render
- Deployment is tied to the `staging` branch
- The pipeline runs tests first
- Only after tests pass does deployment happen
- The staging app is accessible by URL after Render deploys it

---

## Suggested Report Structure

Use the following structure for your PDF submission.

### 1. Title Page

Include:

- assignment title
- your name
- student index number
- course name
- submission date

### 2. Repository Link

Add:

- your fork URL

Example:

- https://github.com/anjananadee23/ci-cd-tutorial-sample-app

### 3. Staging Environment Link

Add:

- the Render URL or other staging URL where the app runs

Example format:

- `https://your-app-name.onrender.com`

### 4. CI Evidence

Include screenshots of:

- a successful GitHub Actions CI run
- the test output showing pass/fail status

### 5. CD Evidence

Include screenshots of:

- a successful staging deployment run
- the running app in the staging environment
- the URL in the browser

### 6. Explanation

Describe:

- why GitHub Actions was chosen for CI/CD
- why Render was chosen for staging
- how the workflow is structured
- how deployment is blocked until tests pass

### 7. Challenges and Fixes

Mention issues such as:

- dependency version conflicts
- application context needed for database operations
- workflow gating for deployment

Explain how each issue was fixed.

### 8. Group Member Details

Add:

- member names
- index numbers

---

## Common Mistakes to Avoid

- forgetting to push to the branch that triggers the workflow
- using incompatible Python package versions
- running tests without an application context when DB access is needed
- deploying before the tests pass
- forgetting to add Render secrets to GitHub
- not including a working staging URL in the report

---

## Final Checklist Before Submission

- [ ] fork created
- [ ] local clone completed
- [ ] meaningful app change committed
- [ ] tests pass locally
- [ ] CI workflow passes on GitHub Actions
- [ ] CD workflow deploys to staging
- [ ] staging URL works in browser
- [ ] report contains repository link
- [ ] report contains staging URL
- [ ] report contains CI screenshot
- [ ] report contains CD screenshot
- [ ] report explains tools, steps, and challenges
- [ ] report includes group member names and index numbers

---

## Short Summary

This assignment is completed properly when you can show all three of these:

1. A forked repository with a meaningful change.
2. A CI pipeline that automatically runs tests on every commit.
3. A CD pipeline that deploys to a live staging environment only after tests pass.

That is the core requirement the grader will look for.
