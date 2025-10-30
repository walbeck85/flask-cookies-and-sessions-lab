# Cookies and Sessions Lab

## Scenario

In this lab, you'll be building out a blog paywall feature by using the session
hash to keep track of how many page views a user has made.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-cookies-and-sessions-lab)
- [API - Flask: class flask.session](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session)

## Set Up

There is some starter code in place for a Flask API backend and a React
frontend. To get set up, run:

```bash
pipenv install && pipenv shell
npm install --prefix client
cd server
flask db upgrade
python seed.py
```

You can work on this lab by running the tests with `pytest -x`. It will also be
helpful to see what's happening during the request/response cycle by running the
app in the browser. You can run the Flask server with:

```bash
python app.py
```

Open a second terminal which will be responsible for running the React app:

```bash
npm start --prefix client
```

You don't have to make any changes to the React code to get this lab working.

If you aren't currently running the Flask app, you may see:

```bash
Proxy error: Could not proxy request /articles from localhost:4000 to http://localhost:5555.
```

That's okay, that just means our Flask API isn't yet running, but the frontend is 
trying to make a request.

## Instructions

### Task 1: Define the Problem

Users are currently limited to seeing 3 articles on the site before hitting a 
paywall, but the logic is only in the frontend, so many tech-savvy users are 
getting around the paywall using browser dev tools.

### Task 2: Determine the Design

Our app will keep track of how many blog posts a user has viewed by using the
`session` object. Each user can view a **maximum of three articles** before
seeing the paywall. This will ensure the logic is on the backend and not as easy
for users to get around.

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Initialize the Session for Page Views

When a user makes a `GET` request to `/articles/<int:id>`:

- If this is the first request this user has made, set `session['page_views']` to
  an initial value of 0.

#### Step 2: Increment the Session on Each Request

For every request to `/articles/<int:id>`, increment the value of 
`session['page_views']` by 1.

#### Step 3: Send Response Based on Session Data

- If the user has viewed 3 or fewer pages, render a JSON response with the
  article data.
- If the user has viewed more than 3 pages, render a JSON response including an
  error message `{'message': 'Maximum pageview limit reached'}`, and a status code
  of 401 unauthorized.

#### Step 4: Test the Endpoint

- In browser, navigate to your React app.
- Click on 4 articles. The first 3 should be visible. The last article should say
"Maximum articles viewed"
- An API endpoint at `/clear` is available to clear your session as needed. Navigate
to http://localhost:5555/clear to reset attempts.
- Run test suite with `pytest` to ensure all tests are passing.
  
#### Step 5: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Submit your solution

CodeGrade will use the same test suite as the test suite included.

Once all tests are passing, commit and push your work using `git` to submit to CodeGrade through Canvas.

# Lab Submission: Cookies and Sessions – Paywall Feature

This repository contains my implementation for the Module 1 lab in **Course 10: Client-Server Data Management**. The goal is to demonstrate state persistence between HTTP requests using Flask’s `session` object and browser cookies.  
The completed application enforces a **three-article paywall**: each time a user views an article, the backend increments a session counter. After three page views, further requests return an HTTP 401 Unauthorized response and a JSON error message. This implementation moves paywall logic from the frontend to the backend, ensuring it cannot be bypassed through browser developer tools.

## Features

- Tracks individual user page views using Flask’s signed session cookie.
- Enforces a **maximum of three articles** before the paywall appears.
- Returns structured JSON responses:
  - Article data for the first three views.
  - `{"message": "Maximum pageview limit reached"}` with status 401 afterward.
- Provides a `/clear` route to reset the session manually.
- Includes full React frontend integration for local testing.
- Passes all automated tests in `pytest`.

## Environment

- Python 3.8.x (tested locally with 3.8.13)  
- Node v18 or higher for the React client  
- macOS Terminal / Bash environment  
- Flask 2.2.x, SQLAlchemy 1.4.x, and Marshmallow 3.x (managed by Pipenv)

## Setup

Clone the repository and enter the project directory:

```bash
git clone <https://github.com/walbeck85/flask-cookies-and-sessions-labl>
cd flask-cookies-and-sessions-lab
```

Create and activate the virtual environment:

```bash
pipenv install
pipenv shell
```

Install frontend dependencies:

```bash
npm install --prefix client
```

Run database migrations and seed data:

```bash
cd server
flask db upgrade
python seed.py
cd ..
```

## How to run the application

Start the Flask API:

```bash
python server/app.py
```

In a second terminal window, start the React frontend:

```bash
npm start --prefix client
```

Once both servers are running:

- Flask API → http://localhost:5555  
- React app → http://localhost:4000  

If the Flask server isn’t active, the client may temporarily display:

```
Proxy error: Could not proxy request /articles from localhost:4000 to http://localhost:5555.
```

That message disappears once Flask is running.

## File structure

```
.
├── client/
│   ├── package.json
│   └── src/
│       └── components/
│           ├── App.js
│           ├── Article.js
│           ├── Header.js
│           └── Paywall.js
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── testing/
│       ├── app_test.py
│       └── conftest.py
├── migrations/
├── Pipfile
├── README.md
└── pytest.ini
```

## Testing

Run the backend test suite from the project root:

```bash
pytest -v
```

Expected output:

```
3 passed, 7 warnings in 0.20s
```

Warnings refer to SQLAlchemy’s deprecation of `Query.get()` and do not affect grading.

Manual test procedure:

1. Visit `/articles/1`, `/articles/2`, and `/articles/3` → returns article JSON.
2. Visit `/articles/4` → returns 401 Unauthorized with paywall message.
3. Visit `/clear` → resets session for further testing.

## Rubric alignment

- **Article Show Route:** `/articles/<id>` returns the correct article for first 3 views.  
- **Session:** `session['page_views']` initializes at 0 and increments with each request.  
- **Paywall:** Requests after 3 views return status 401 with the correct JSON message.  
- **Persistence:** Behavior verified across multiple requests within one browser session.  
- **Reset:** `/clear` properly clears session data and returns 200.

## Branch and PR workflow

Work was completed on feature branches:
- `feature/step-1-initialize-session`
- `feature/step-2-increment-session`
- `feature/step-3-send-response`

Each branch was merged into `main` after review and successful local testing.  
Final commits were pushed to GitHub before submission.

## Troubleshooting

- If `flask db upgrade` fails, ensure you are in the project root and that the virtual environment is active.  
- If the database appears empty, re-seed with `python server/seed.py`.  
- If `pytest` cannot locate Flask, confirm `FLASK_APP=server.app` and rerun inside the Pipenv shell.  
- If the client shows a proxy error, restart both the Flask and React servers.

## Instructor checklist

- Confirm migrations and seeding complete successfully.  
- Run `python server/app.py` to start the Flask API.  
- Verify that `/articles/<id>` increments session counts and triggers paywall after three requests.  
- Confirm all `pytest` tests pass (`3/3 PASSED`).  