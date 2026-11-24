# ACEest Fitness & Gym

ACEest Fitness & Gym is a small Flask application that exposes gym member, membership plan, health, and check-in endpoints. It is also a DevOps example with automated tests, a Docker image, a GitHub Actions workflow, and a Jenkins pipeline.

The application is API-first. The home page links to the available endpoints; member and plan data are returned as JSON. There is no sign-in or graphical member-management interface.

## What You Need

- Python 3.12 (recommended; used by Docker and GitHub Actions)
- Git
- Docker, if you want to build or run the container

## Run the Application Locally

1. Clone the repository and enter its directory:

   ```bash
   git clone https://github.com/2026ht66002/devops-assignment.git
   cd devops-assignment
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, use `.venv\Scripts\Activate.ps1`.

3. Install dependencies and start the server:

   ```bash
   python -m pip install -r requirements.txt
   python app.py
   ```

4. Open [http://localhost:5000](http://localhost:5000). Keep the server terminal open while using the app; press `Ctrl+C` to stop it.

## Use the Application

Open these `GET` routes in a browser or request them with `curl`. The examples assume the local server is running.

| Route           | What it does                                         |
| --------------- | ---------------------------------------------------- |
| `GET /`         | Shows the application name and route links.          |
| `GET /health`   | Returns the service health status.                   |
| `GET /members`  | Returns sample members, their IDs, status, and plan. |
| `GET /plans`    | Returns the plans, fees, and included access.        |
| `POST /checkin` | Checks in a member using a JSON request body.        |

```bash
curl http://localhost:5000/health
curl http://localhost:5000/members
curl http://localhost:5000/plans
```

To check in a sample member (`M101`, `M102`, `M103`, or `M104`), send its ID as JSON:

```bash
curl -X POST http://localhost:5000/checkin \
  -H "Content-Type: application/json" \
  -d '{"member_id":"M101"}'
```

A successful request returns the member ID, name, plan, and `checked_in` status. A missing ID returns HTTP `400`; an unknown member ID returns HTTP `404`. Check-in state is held in memory and resets when the process restarts; it is not stored in a database.

## Run the Tests

With the virtual environment active, run:

```bash
python -m pytest -q
```

The tests cover the home page, health, members and plans responses, successful check-in, and invalid check-in requests.

## Run with Docker

Build and start the container from the repository root:

```bash
docker build -t aceest-fitness-gym .
docker run --rm -p 5000:5000 aceest-fitness-gym
```

Visit [http://localhost:5000](http://localhost:5000) or request `http://localhost:5000/plans`. The container runs Gunicorn as a non-root user. Press `Ctrl+C` to stop it.

## Automated Build and Test

### GitHub Actions

The workflow at `.github/workflows/main.yml` runs on pushes and pull requests. It checks out the code, sets up Python 3.12, installs dependencies, checks Python syntax, runs tests, builds the Docker image, starts a container, and requests `/plans`. It verifies the build but does not publish an image or deploy the service.

### Jenkins

The `Jenkinsfile` installs dependencies, runs Pytest, analyzes the project with SonarQube, builds and pushes the Docker image, then deploys it to Minikube. The current pipeline runs SonarQube analysis but does not wait for a Quality Gate result or generate a coverage report. Create a Jenkins Pipeline job that loads this `Jenkinsfile` from the repository, using `https://github.com/2026ht66002/devops-assignment.git` and the `main` branch. For a private repository, configure access through Jenkins Credentials; do not store passwords in the repository.

Configure a Jenkins SonarQube server named `SonarQube`, a SonarScanner tool named `SonarScanner`, and a secret-text credential with ID `sonar-qube-token`. Add a username/password credential with ID `dockerhub-credentials` for Docker Hub; keep all tokens and passwords in Jenkins Credentials rather than in source control.

The Jenkins agent needs Python 3, the Docker CLI, access to a Docker daemon, and `kubectl` configured with a `minikube` context that the agent can reach. The Minikube CLI itself is not required in Jenkins. The pipeline pushes both `latest` and the Jenkins build-number tags to the public Docker Hub repository `2026ht66002/devops-assignment-2`, then applies [k8s/minikube.yaml](./k8s/minikube.yaml) to create or update the `aceest-fitness-gym` Deployment and NodePort Service. The deployment uses `imagePullPolicy: Always`. If Jenkins runs in a container, persist `/var/jenkins_home`, install `kubectl` under `/var/jenkins_home/bin`, and provide `/var/jenkins_home/.kube/config` with a Minikube API endpoint reachable from that container.

After a successful deployment, get the application URL with:

```bash
minikube service aceest-fitness-gym --url
```

## Screenshot Walkthrough

These screenshots are grouped by workflow and are chronological where timestamps are available. Each numbered step describes the action shown immediately below it.

### Repository and Tests

**Step 1: Create an SSH key and attempt to clone the repository.** The remote is empty at this point, as the terminal reports.

![Generating an SSH key and attempting to clone the empty repository](ScreenShots/Screenshot_2026-10-07_01-18-10.png)

**Step 2: Inspect the project files and commit the initial Flask application and requirements.**

![Checking the project files and creating the initial commit](ScreenShots/Screenshot_2026-10-07_01-24-00.png)

**Step 3: Rename the branch to `main` and push it to GitHub.**

![Renaming and pushing the main branch](ScreenShots/Screenshot_2026-10-07_01-24-45.png)

**Step 4: Create `feature/unit-test`, add the tests directory, and commit the application tests.**

![Creating the unit test branch and committing the tests](ScreenShots/Screenshot_2026-10-07_01-33-39.png)

**Step 5: Push `feature/unit-test`, merge it into `main`, and push the updated main branch.**

![Pushing and merging the unit-test branch into main](ScreenShots/Screenshot_2026-10-07_01-34-50.png)

### CI/CD Branch and Local Verification

**Step 6: Create `feature/ci-cd` and check that the Dockerfile and Jenkinsfile are ready to add.**

![Creating the CI/CD branch and checking the working tree](ScreenShots/Screenshot_2026-10-07_01-39-17.png)

**Step 7: Commit the Dockerfile and Jenkinsfile on `feature/ci-cd`, then push the branch to GitHub.**

![Committing and pushing the Dockerfile and Jenkinsfile](ScreenShots/Screenshot_2026-10-07_01-40-26.png)

**Step 8: Switch to `main` and merge `feature/ci-cd`, adding the Dockerfile and Jenkinsfile to the main branch.**

![Merging the CI/CD branch into main](ScreenShots/Screenshot_2026-10-07_01-40-51.png)

**Step 9: Build the image as `gym-app` and start it in the background, mapping host port `5000` to container port `5000`.**

![Building the gym-app image and starting its container](ScreenShots/Screenshot_2026-10-07_01-48-34.png)

**Step 10: Request `/plans` from the running container and confirm the response includes the Basic, Premium, and Elite plans.**

![Requesting the plans endpoint](ScreenShots/Screenshot_2026-10-07_01-52-24.png)

### Jenkins

**Step 11: Create a Jenkins item named `aceest-gym-cicd` and select the Pipeline type.**

![Creating the Jenkins Pipeline item](ScreenShots/Screenshot_2026-10-07_01-54-33.png)

**Step 12: In Jenkins, add a credential containing your GitHub username and password for repository access.** Do not copy or expose credentials from screenshots.

![Adding a Jenkins repository credential](ScreenShots/Screenshot_2026-10-07_01-58-17.png)

**Step 13: Configure the repository URL, select the credential, and specify the `main` branch.**

![Configuring the Jenkins repository and main branch](ScreenShots/Screenshot_2026-10-07_01-59-25.png)

**Step 14: Run the Jenkins pipeline and confirm checkout, dependency installation, tests, and Docker image build succeed.**

![Successful Jenkins pipeline run](ScreenShots/Screenshot_2026-10-07_02-18-34.png)

### GitHub Actions

**Step 15: Add and commit the GitHub Actions workflow on the CI/CD branch.**

![Committing the GitHub Actions workflow](ScreenShots/Screenshot_2026-10-07_02-29-51.png)

**Step 16: Confirm that the GitHub Actions job succeeds through the Docker image build.**

![Successful GitHub Actions build and test job](ScreenShots/Screenshot_2026-10-07_02-43-26.png)

**Step 17: Confirm that the workflow runs the Docker image and requests `/plans`, receiving the plans JSON.**

![GitHub Actions running the image and checking the plans endpoint](ScreenShots/Screenshot_2026-10-07_02-56-39.png)

### SonarQube, Docker Hub, and Minikube

**Step 18: Generate a SonarQube token for Jenkins authentication.** Save it as the Jenkins secret-text credential `sonar-qube-token`; never commit the token to the repository.

![SonarQube token generation screen](ScreenShotsAssignment2/Screenshot_2026-11-24_18-17-50.png)

**Step 19: Install the SonarQube Scanner integration in Jenkins.** The screenshot shows the Scanner and Quality Gates plugins being installed.

![Installing SonarQube-related Jenkins plugins](ScreenShotsAssignment2/Screenshot_2026-11-24_18-19-26.png)

**Step 20: Configure the Jenkins SonarScanner tool.** Use the name `SonarScanner` to match the `tool` reference in the Jenkinsfile.

![Configuring the SonarScanner tool in Jenkins](ScreenShotsAssignment2/Screenshot_2026-11-24_18-24-55.png)

**Step 21: Add the SonarQube server in Jenkins.** Name the server `SonarQube` and select the `sonar-qube-token` credential.

![Configuring the SonarQube server in Jenkins](ScreenShotsAssignment2/Screenshot_2026-11-24_18-30-56.png)

**Step 22: Run the initial Jenkins analysis and Docker build.** This recorded build completes checkout, dependency installation, tests, SonarQube analysis, and Docker image build.

![Initial Jenkins pipeline run through the Docker build](ScreenShotsAssignment2/Screenshot_2026-11-24_19-27-41.png)

**Step 23: Review the SonarQube project report.** This snapshot shows security findings to review; successful analysis does not mean there are no issues.

![SonarQube project security overview](ScreenShotsAssignment2/sonar1.png)

**Step 24: Add Docker Hub credentials in Jenkins.** Use a username/password credential with ID `dockerhub-credentials`; do not expose the password in screenshots or source control.

![Adding Docker Hub credentials in Jenkins](ScreenShotsAssignment2/Screenshot_2026-11-24_19-42-24.png)

**Step 25: Confirm the Jenkins pipeline pushes the Docker image to the registry.**

![Successful Jenkins run that pushes the Docker image](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 8.55.42 PM.png>)

**Step 26: Verify that Docker Hub contains the `latest` and build-number tags.**

![Docker Hub repository tags](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 8.58.33 PM.png>)

**Step 27: Review a successful Jenkins run that includes a Quality Gate stage.** This is a captured earlier pipeline run; the current Jenkinsfile performs SonarQube analysis but does not include `waitForQualityGate`.

![Earlier Jenkins pipeline run with a Quality Gate stage](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 9.05.23 PM.png>)

**Step 28: Start Minikube and confirm the cluster is ready.** The Minikube CLI runs on the host; Jenkins uses `kubectl` to deploy to the cluster.

![Starting the Minikube cluster](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 10.12.37 PM.png>)

**Step 29: Confirm Jenkins applies the Kubernetes manifest and waits for the deployment rollout.**

![Successful Jenkins deployment to Minikube](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 10.49.52 PM.png>)

**Step 30: Review the SonarQube project overview after the deployment run.**

![SonarQube overview after the final pipeline run](<ScreenShotsAssignment2/Screenshot 2026-11-24 at 10.51.25 PM.png>)

## Project Files

- `app.py` contains the Flask routes and sample data.
- `tests/test_app.py` contains the automated endpoint tests.
- `Dockerfile` defines the container image.
- `k8s/minikube.yaml` defines the Minikube Deployment and NodePort Service.
- `.github/workflows/main.yml` defines GitHub Actions validation.
- `Jenkinsfile` defines the Jenkins build pipeline.
- `ScreenShots/` and `ScreenShotsAssignment2/` contain the project walkthrough images.

## License

This project is for academic learning and assignment submission purposes.
