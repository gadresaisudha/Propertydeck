# Propertydeck

App Design
Test Driven Development intro
System setup
project setup
configure github actions
Test Driven Development with django
configure database
create user model
setup django admin
API documentation
Build user api
Build property api
Build review api
Build Favourite api
Build Listing inquiry api
Build image api
Implement filtering
Deployment to AWS

Mostly focused on building rest apis that can be called from frontend either from webapp or mobileapp

Features:
api endpoints
user authentication
browsable admin interface(Django admin)
browsable api(swagger)

Tech stack:
programming language : python(foundation api)
web framework : Django(Handles URL mapping, object relational mapper, admin site), Django Rest framework(add on to build rest apis), use  django orm to crud objects in database
database : postgressql
containerization: using docker one for api and another for database(easily allows us to create dev environment and deployment)
documentaion: Swagger api(automated documentation), Browsable api(testing)
automation: github actions(Testing and linting)

project structure:
app/- main django project
app/core/- code shared between multiple apps(database definations)
app/user/- user related code
app/property/- property app
app/review/- review app
app/inquiry/ - inquiry app
app/favourite/ - favourite app

applications on your local machine:
vscode
docker desktop
git 

confirmation of this installation:
check for vscode
command prompt:
docker --version
docker-compose --version
git --version


make sure you have github account and docker hub account
create a github project:
go to github -> create repository, add readme.md,mit license and also gitignore with python
now get the ssh clone url copy it
now in local machine:
>>>> git clone "url"
project gets clone to local repository


create a docker hub account:
login and go to profile -> security -> generate access token
so that you dont have to provide password for the github to authenticate into docker and do whatever it needs
new access token
->with read,write,delete repository
it will generate a username and access token
these are the authentication details for our docker hub

now these details need to be configured on our github repository
go to settings->secrets and variables->actions->
create a repository secret
DOCKERHUB_USER , sudhagadre 
create another repository secret
DOCKERHUB_TOKEN , fmdjsghnerkl;vs,rfdgl;bdmd
These details are very much essential when configuring github actions

open your project in vsscode:
Create a requirements.txt File:

In the project root, create a file named requirements.txt.
Add Package Requirements:

Define the Django version:
Django>=3.2.4,<=3.3
Define the Django Rest Framework version:
djangorestframework>=3.12.4,<=3.13
Key Points:
Version Pinning:
Use specific version ranges to ensure compatibility and avoid breaking changes from major version upgrades.
The syntax ensures you get the latest patch updates for bug fixes and security fixes without jumping to the next minor version.
Real-World Scenario:
Working with fixed versions mirrors real-world software development where projects often start with one version and upgrade later for maintenance.
Best Practices:
Save the requirements.txt file after defining the packages.
Follow course-recommended versions to avoid compatibility issues during learning.
This approach ensures stability during development and prepares you for upgrading packages as part of software maintenance.


Explanation of the Dockerfile
The provided Dockerfile defines the instructions needed to create a Docker image for a Python-based Django application. Below is a step-by-step explanation of each section:

1. Base Image
dockerfile
Copy code
FROM python:3.9-alpine3.13
Specifies the base image from Docker Hub.
python:3.9-alpine3.13 is a lightweight version of Python 3.9 bundled with Alpine Linux 3.13.
Alpine Linux is used because of its minimal footprint, making it efficient for Docker images.
2. Metadata
dockerfile
Copy code
LABEL maintainer="propertydeck.com"
Adds metadata about the image.
The maintainer label identifies the person or organization responsible for the Docker image. In this case, it points to propertydeck.com.
3. Environment Configuration
dockerfile
Copy code
ENV PYTHONUNBUFFERED 1
Ensures Python outputs directly to the terminal without buffering.
This helps when debugging or logging, as outputs are displayed immediately.
4. File Copy
dockerfile
Copy code
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
COPY ./requirements.txt /tmp/requirements.txt: Copies the requirements.txt file from the project directory to the /tmp/ directory in the container.
COPY ./app /app: Copies the app directory (the Django project) into the /app directory inside the container.
WORKDIR /app: Sets the working directory to /app. All subsequent commands will be run relative to this directory.
5. Exposing Ports
dockerfile
Copy code
EXPOSE 8000
Exposes port 8000 of the container to the host system.
This is the default port for the Django development server, allowing the host machine to access the application.
6. Installation and Setup
dockerfile
Copy code
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
Virtual Environment:

Creates a Python virtual environment at /py using python -m venv /py.
Helps isolate dependencies from the base Python environment.
Upgrade Pip:

Upgrades pip inside the virtual environment.
Install Dependencies:

Installs Python dependencies listed in /tmp/requirements.txt using the virtual environment’s pip.
Cleanup:

Deletes the /tmp directory to minimize the image size.
Add Non-Root User:

Creates a user django-user with no password and no home directory.
Running the application as a non-root user enhances security by limiting privileges if the application is compromised.
7. Update PATH
dockerfile
Copy code
ENV PATH="/py/bin:$PATH"
Updates the PATH environment variable to include /py/bin.
Allows commands like python and pip to be run without specifying the full path.
8. Default User
dockerfile
Copy code
USER django-user
Switches to the django-user created earlier.
Ensures all subsequent processes in the container run with limited privileges, following Docker best practices.
Summary
This Dockerfile creates a lightweight and secure image tailored for a Django application. It uses Alpine Linux to keep the size minimal and sets up a Python virtual environment to avoid dependency conflicts. Security is enhanced by creating a non-root user and cleaning up temporary files during the build process. The exposed port allows the application to be accessible via port 8000 on the host system.



The provided list appears to be a .gitignore file configuration. Here's an explanation of what each section does and its significance:

1. Git
plaintext
Copy code
.git
.gitignore
.git: This would ignore the .git folder, effectively breaking version control for the repository if used. However, adding .git to a .gitignore file is unnecessary unless it’s mistakenly included.
.gitignore: The .gitignore file itself should not be ignored. It is used to specify which files or directories should not be tracked by Git. This entry might have been added by mistake.
2. Docker
plaintext
Copy code
.docker
Ignores the .docker directory, likely used for local Docker-related configuration files or artifacts not meant to be committed to the repository.
3. Python
plaintext
Copy code
app/__pycache__/
app/*/__pycache__/
app/*/*/__pycache__/
app/*/*/*/__pycache__
Ignores Python's __pycache__ directories, which contain cached bytecode files (.pyc). These files are automatically generated by Python to optimize code execution but should not be committed.
plaintext
Copy code
.env
Ignores .env files, typically used to store environment variables. These files may contain sensitive information, such as API keys or database credentials, and should not be included in version control.
plaintext
Copy code
.venv/
venv/
Ignores virtual environment directories. Virtual environments contain local dependencies and configurations specific to the system and should not be included in the repository.
Recommended Adjustments
Here’s an updated version of the .gitignore file with improvements:

plaintext
Copy code
# Git
# The `.git` folder is essential and should not be ignored.
# Removed `.git`.

# Docker
.docker

# Python Cache
**/__pycache__/

# Environment Files
.env

# Virtual Environments
.venv/
venv/
Key Notes
Avoid adding .git to the .gitignore file as it is critical for version control.
The use of wildcards (*) for multiple directory levels can be simplified to **.
Ensure .env files are included in .gitignore to prevent sensitive data from being exposed.

create a new folder on local machine app
open docker desktop login
open docker hub and login

terminal >>docker login
>>>docker build .

This builds image for our application


This docker-compose.yml file defines the configuration for running a containerized application with Docker Compose.

Breakdown of the File:
yaml
Copy code
version: "3.9"
Specifies the version of the Docker Compose file syntax being used.
Reason: Ensures compatibility and provides access to features available in version 3.9.
yaml
Copy code
services:
  app:
Declares the services needed for the application.
app: The name of the service running the application. It maps to the settings specified in the block below.
Build Configuration:
yaml
Copy code
    build:
      context: .
build: Defines the build configuration for the app service.
context: .: Specifies the directory (. = current directory) containing the Dockerfile.
Ports Mapping:
yaml
Copy code
    ports:
    - "8000:8000"
Maps port 8000 on the host machine to port 8000 inside the container.
Purpose: Allows access to the application running in the container through localhost:8000.
Volumes Mapping:
yaml
Copy code
    volumes:
    - ./app:/app
Maps the app directory on the host machine (./app) to the /app directory inside the container.
Purpose: Synchronizes changes made to local files with the container in real-time, so there’s no need to rebuild the container after every code change.
Command to Run the Application:
yaml
Copy code
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"
Purpose: Runs the Django development server inside the container.
Details:
sh -c: Executes the specified command inside a shell.
python manage.py runserver 0.0.0.0:8000: Starts the Django server, making it accessible on all network interfaces (0.0.0.0) at port 8000.
Steps to Build and Run:
Build the Containers:

bash
Copy code
docker-compose build
Builds the images based on the Dockerfile and tags them for use in the docker-compose configuration.
Run the Application:

bash
Copy code
docker-compose up
Starts the container and runs the service as defined.
Access the Application:

Open your browser and navigate to http://localhost:8000 to see the application running.
Stop the Application:

bash
Copy code
docker-compose down
Stops and removes the container and network created by docker-compose.
This setup enables efficient development by syncing files and provides a clean, consistent environment for running the application.


Linting with Flake8
Linting ensures your code adheres to formatting and style standards. We'll use Flake8 as our linting tool.

Steps to Implement Linting:
Install Flake8: Run the command to add Flake8 to your project dependencies:

bash
Copy code
pip install flake8
Run Flake8 with Docker Compose: Add the following syntax to run Flake8 in your Docker Compose setup:

bash
Copy code
docker-compose run app sh -c "flake8"
Understand the Output:

Errors will be displayed with file paths, line numbers, and issue descriptions.
Example:
bash
Copy code
app/serializers.py:57:18: E231 missing whitespace after ','
File: serializers.py
Line: 57
Issue: Missing whitespace after a comma.
Fix Linting Errors:

Fix errors starting from the bottom up. This avoids line number mismatches caused by adding/removing lines.
Testing with Django Test Suite
Testing ensures your application behaves as expected. We'll use Django's built-in test framework.

Steps to Implement Testing:
Write Tests:

Add test cases for each Django app in tests.py.
Example test case:
python
Copy code
from django.test import TestCase
from .models import MyModel

class MyModelTestCase(TestCase):
    def test_model_creation(self):
        instance = MyModel.objects.create(name="Test Instance")
        self.assertEqual(instance.name, "Test Instance")
Run Tests with Docker Compose: Use the following command to run tests:

bash
Copy code
docker-compose run app sh -c "python manage.py test"
Interpret Test Results:

Passing tests will show a summary like:
Copy code
Ran 3 tests in 0.002s
OK
Failing tests will include detailed error messages and stack traces.
Best Practices:
Automate Linting and Testing: Set up a pre-commit hook or CI pipeline to run linting and tests automatically.
Fix Issues Iteratively:
Address linting errors and rerun flake8.
Fix failing tests and rerun the test suite until all pass.


Here's a concise summary and step-by-step guide for configuring your project to use Flake8 for linting and testing:

1. Create a Development Requirements File
File: requirements.dev.txt
Content: Add Flake8 version constraints:
shell
Copy code
flake8>=3.9.2,<=3.10
Reason: Separate development dependencies from production to avoid unnecessary bloat and ensure secure deployment.
2. Update Docker Configuration
a. Update docker-compose.yml
Add a build argument for development mode:
yaml
Copy code
build:
  context: .
  args:
    - dev=true
b. Modify Dockerfile
Add a default build argument:
dockerfile
Copy code
ARG dev=false
Install requirements.dev.txt conditionally:
dockerfile
Copy code
COPY requirements.dev.txt /tmp/requirements.dev.txt

RUN if [ "$dev" = "true" ]; then \
      pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp/requirements.dev.txt
Purpose: Ensure flake8 is only installed in development environments.
3. Create Flake8 Configuration
File: .flake8 (in the app directory)
Content:
ini
Copy code
[flake8]
exclude = migrations, __pycache__, manage.py, settings.py
Reason: Exclude auto-generated files from linting.
4. Test the Setup
a. Build Docker Image
bash
Copy code
docker-compose build
Fix Errors: If the build fails, check file paths or syntax in the Docker configuration.
b. Run Flake8
bash
Copy code
docker-compose run --rm app sh -c "flake8"
Expected Result: No output (no linting errors)


Here’s a streamlined guide to creating your Django project using Docker Compose, along with key points about the process:

1. Run the Django Project Creation Command
Open your terminal or command prompt and type the following command to create the Django project:

bash
Copy code
docker-compose run --rm app sh -c "django-admin startproject app ."
Explanation of the Command:
docker-compose run: Starts the specified service in Docker Compose.
--rm: Automatically removes the container after the command is executed, keeping things clean.
app: Refers to the app service defined in your docker-compose.yml.
sh -c: Allows you to pass shell commands to the container.
django-admin startproject app .: Runs the Django CLI to create a new project named app in the current directory (.).
2. Ensure the Directory Structure
After running the command, your project directory should look like this:

markdown
Copy code
project-root/
├── app/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __pycache__/
├── manage.py
├── requirements.txt
├── requirements.dev.txt
├── Dockerfile
├── docker-compose.yml
Key Points:
The dot (.) in the command ensures that the app directory (containing settings.py, etc.) is created in the root of the project, avoiding unnecessary nested directories.
The manage.py file is placed alongside the app directory.
3. How File Sync Works
Volume Mapping: In docker-compose.yml, a volume maps the host app/ directory to the container's app/. This syncs files between your local machine and the Docker container.
yaml
Copy code
volumes:
  - ./app:/app
Two-Way Sync: Changes made in the container reflect in your local files, and vice versa.
4. Verify the Project
To ensure the Django project was created successfully:

Check the project files in the app directory.
Run the following command to confirm that Django recognizes the project:
bash
Copy code
docker-compose run --rm app sh -c "python manage.py check"
If no errors are reported, your Django setup is correct.


Here’s a concise guide to running your Django development server using Docker Compose and verifying its functionality:

1. Start the Development Server
Run the following command in your terminal or command prompt to start the services defined in docker-compose.yml:

bash
Copy code
docker-compose up
What Happens:
Docker Compose starts the app service (or other services defined in your Compose file).
The app service runs the Django development server, typically on port 8000.
2. Access the Development Server
Open a browser and go to:
http://127.0.0.1:8000
(This is equivalent to http://localhost:8000.)
You should see the default Django welcome page with the rocket icon, confirming your setup is correct.
3. Monitor Logs
In the terminal, you'll see logs from the Django server, including HTTP requests like:
csharp
Copy code
[04/Jan/2025 12:34:56] "GET / HTTP/1.1" 200 OK
Each browser refresh outputs additional logs, indicating communication between your browser and the server.
4. Stopping the Server
To stop the server:

Press Ctrl + C in the terminal running docker-compose up.
This halts all running services and stops the Django server.
If you refresh the browser, you'll see an error like:

Copy code
This site can’t be reached
5. Restarting the Server
To restart:

Run:
bash
Copy code
docker-compose up
Refresh the browser until the page reloads.
Troubleshooting Tips
Service Taking Time to Start:
If the server doesn't load immediately, give it a moment to initialize. Check the terminal logs for progress.

Check for Port Conflicts:
If 8000 is in use, you can modify the port in your docker-compose.yml by mapping a different local port to the container's port:

yaml
Copy code
ports:
  - "8080:8000"
Then access the server at http://127.0.0.1:8080.

With this setup, your Django project should run seamlessly in a Dockerized environment. Let me know if you face any issues or need further guidance!


Summary
We set up a recipe app project by creating a GitHub repository and adding Docker Hub credentials for CI. Locally, we added a Dockerfile, docker-compose.yml, and requirements.txt. A new Django project was initialized using Docker, ensuring the correct directory structure. Flake8 was configured for code linting, and the development server was successfully run with docker-compose up, confirming the setup.

Summary of GitHub Actions Overview
In this section, we learned about GitHub Actions, a CI/CD automation tool for GitHub, comparable to tools like Jenkins or GitLab CI/CD. GitHub Actions automates tasks such as deployment, code linting, and unit testing triggered by events like code pushes.

Key points include:

Trigger Setup: We’ll use the "push" trigger to initiate jobs when code changes are pushed to GitHub.
Jobs: Automate tasks like running unit tests or code linting. Jobs provide a pass/fail output, indicating success or the need for changes.
Pricing: GitHub Actions offers 2000 free minutes monthly for free accounts, sufficient for small projects or this course. Additional minutes can be purchased if needed for extensive use.
In this course, we'll focus on automating code linting and unit testing with GitHub Actions.



Summary of Configuring GitHub Actions for Docker Authentication
In this lesson, we discussed setting up GitHub Actions and authenticating with Docker Hub to handle rate limits effectively.

Key steps:

Config File Creation:

Place the configuration file in .github/workflows/ and name it something like checks.yml (must end with .yml).
This file defines triggers and steps for running tests and linting.
Docker Hub Rate Limits:

Anonymous Users: Limited to 100 pulls per 6 hours, identified by IP address.
Authenticated Users: Get 200 pulls per 6 hours, unaffected by shared IP addresses (e.g., GitHub Actions' shared IPs).
Authentication with Docker Hub:

Sign up for a free Docker Hub account at hub.docker.com.
Use Docker login credentials in GitHub Actions to authenticate and increase pull limits.
This ensures 200 pulls are exclusively available to your project.
GitHub Secrets:

Add credentials (e.g., Docker Hub username and access token) as Secrets in your GitHub repository.
These secrets are encrypted and securely stored, accessible only during GitHub Actions runs.
By authenticating with Docker Hub, you ensure smoother builds with adequate pull limits, avoiding issues caused by shared IP rate limits. The next lessons will detail the implementation process for these configurations.


Summary of Creating GitHub Actions Configuration
In this lesson, we walked through the steps for creating a GitHub Actions configuration file to set up automated processes for testing and linting your project, while also authenticating with Docker Hub.

Here’s a breakdown of what you need to do:

Folder Structure:

Create a folder structure: .github/workflows/.
Inside this folder, create the configuration file (e.g., checks.yml).
Define Triggers:

Set the trigger to run the actions on a push event:
yaml
Copy code
on: 
  push:
Create Jobs:

Define a job (e.g., test-lint) that will run on the Ubuntu 20.04 runner:
yaml
Copy code
jobs:
  test-lint:
    runs-on: ubuntu-20.04
Define Steps:

Log into Docker Hub:

Use a pre-made Docker login action to authenticate with Docker Hub, passing in your Docker Hub credentials stored as GitHub Secrets:
yaml
Copy code
- name: Log into Docker Hub
  uses: docker/login-action@v1
  with:
    username: ${{ secrets.DOCKER_HUB_USER }}
    password: ${{ secrets.DOCKER_HUB_TOKEN }}
Checkout Code:

Use the actions/checkout action to ensure the code is available for the workflow to run tests and linting:
yaml
Copy code
- name: Checkout code
  uses: actions/checkout@v2
Run Tests:

Run unit tests using Docker Compose:
yaml
Copy code
- name: Run tests
  run: docker-compose run --rm app bash -c "python manage.py test"
Run Linting:

Run linting using Docker Compose:
yaml
Copy code
- name: Run lint
  run: docker-compose run --rm app bash -c "flake8"
Handling Failures:

If any of the steps fail (e.g., a test or linting failure), the job will fail and stop execution. This ensures the pipeline won't proceed until issues are resolved.
Pre-installed Tools:

On the Ubuntu 20.04 runner, Docker and Docker Compose are pre-installed, so no need to install them manually in the workflow.
Next Steps
After configuring the workflow, you will need to set up GitHub Secrets to store your Docker Hub username and token securely.
Once the secrets are added and the workflow is committed to your repository, it will trigger on each push, running the defined jobs automatically.
This setup ensures that your code is automatically tested and linted in an isolated Docker environment every time you push changes to your repository.