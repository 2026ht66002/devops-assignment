# ACEest Fitness & Gym DevOps Assignment

This project implements a simple Flask application for the ACEest Fitness & Gym assignment and demonstrates a basic DevOps workflow using Git, GitHub Actions, Docker, and Jenkins.

## Project Objective

The application is designed to simulate a small gym management system and includes:

- Flask web endpoints for a fitness business
- A test suite using Pytest
- Docker containerization
- CI pipeline automation through GitHub Actions
- Jenkins pipeline support for build validation

## Features

- `GET /` - landing page for the gym
- `GET /health` - health check endpoint
- `GET /members` - list all members
- `GET /plans` - list membership plans
- `POST /checkin` - marks a member as checked in

## Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/himanshu-sahu/devops-test.git
   cd devops-test
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:

   ```bash
   python app.py
   ```

5. Open the app in a browser:
   ```text
   http://localhost:5000
   ```

## Run Tests Manually

```bash
python -m pytest -q
```

## Docker Build and Run

Build the image:

```bash
docker build -t aceest-fitness-gym .
```

Run the container:

```bash
docker run -p 5000:5000 aceest-fitness-gym
```

## GitHub Actions Workflow

The workflow in `.github/workflows/main.yml` is triggered on pushes and pull requests to any branch. It performs the following steps:

1. Checks out the code
2. Sets up Python 3.12
3. Installs dependencies from `requirements.txt`
4. Runs a syntax check with `compileall`
5. Executes the Pytest suite
6. Builds the Docker image using `requirements.txt`

The workflow validates and builds the image; it does not publish the image or deploy the application.

## Jenkins Integration

The included `Jenkinsfile` defines a build pipeline that does the following:

1. Checks out the configured SCM repository and installs project dependencies
2. Runs the test suite
3. Builds the Docker image

To run it, create a Jenkins Pipeline job (or Multibranch Pipeline), configure its SCM URL as `https://github.com/himanshu-sahu/devops-test.git`, and use the repository's `Jenkinsfile`. Configure a GitHub webhook or SCM polling in Jenkins if builds should start automatically after pushes. Public repository access does not require GitHub credentials; private repositories do.

The Jenkins agent must have Python 3, the Docker CLI, and permission to use a Docker daemon. If Jenkins runs in a container, configure Docker socket access for the Jenkins process; the pipeline cannot grant that host-level permission itself.

## Assignment Reflection

This project follows the DevOps assignment goals by demonstrating:

- version control readiness with Git
- automated validation with tests
- predictable deployment using Docker
- pipeline automation using GitHub Actions and Jenkins
- clear documentation for onboarding and maintenance

## License

This project is for academic learning and assignment submission purposes.
