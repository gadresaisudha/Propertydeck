Test driven development:
write test -> run test(fails)-> add feature-> run test(passes)-><- re-factor
why use TDD:
better understanding of code
reduce bugs
TDD is a software development practice
in TDD it is write test first then write code

General development:
write code -> write test
these are generally called unit tests


Docker:
why use docker?

Well, there are many benefits to using Docker for development.
One of them is that you have a consistent development and production environment.So with Docker you can use the same image for your development as you use for production.
This means that you're using exactly the same code on production and it eliminates all of those issues
where you might have a problem that occurs on the production server, but you can't reproduce it locally because you're using the same image and the same set of based dependencies. You should have a consistent environment on your local development machine and on the server you deploy.

The application to another benefit is easier collaboration.
Often you'll be working on projects with other developers and there are so many times that I can think of where I've been sharing our project with a developer. And what happens is it works perfectly fine on my machine and everything was normally.
However, when we go to run the project on the other developers machine, they run into a whole world of issues. And this often happens because the dependencies that I run my machine. So dependencies are any software that I'll project depends on a different from the dependencies.On the other developers machine, for example, they might have a different version of Python or they might have a different version of the database we're using, or a different version of some SDK toolthat we're using on the software.And this means that you have a whole load of issues to sort out because you basically need to make sure
all the dependencies are exactly the same on both machines.
However, when you use Docker, this eliminates all of those problems because all your dependencies are inside the Docker image, which is defined in your project. So when the other developer runs your project that is set up to use Docker in almost all cases, it just works. They just run the Docker images and it just works fine.

Another benefit is that using Docker allows you to capture all of the dependencies in the source code of your project.
You don't need to install things manually on your machine and configure them to work with your project. It can all be done in the code. You can define every single dependency that your project needs inside the source code. This again helps with easier collaboration.For example, you can have all of the requirements, your python requirements defined in your project,
and you can also add all of the operating system level dependencies in your Docker file.


Another benefit is easier cleanup.So if you're watching as a professional developer, you'll often be working on various different projects and you might be just working on a project for a set period of time. So let's say you need to spend a couple of weeks working on a particular project. When you use Docker, when you're finished using that project, you can simply just delete the project files and delete all of the Docker images, and then your system is completely cleared of the dependencies that were needed for that project. You don't need to go through and manually remove any SDK or any databases that might be new in your system. It was all contained inside the Docker configuration for that project.

So how are we going to use Docker when we're developing our Django project first will define a doc of all the Docker files, going to contain all of the operating system level dependencies that our project needs. Then we'll create a Docker compose configuration. This will tell Docker how to run the images that are created from our Docker file configuration. We're going to run all the commands that we need for this project through Docker Compose, and I'm going to show you an example of that in a moment. There's one thing to keep in mind when we using Docker with GitHub actions. Docker has something called Docker Hub. Docker Hub is where we can our shared public images down to reuse them for our project. For example, there's an image for Python, like a Python base image for Docker, and that would come from Docker Hub.However, Docker Hub has introduced some rate limits, and a rate limit is basically limiting the amount
of access that you have so that you need to upgrade to pay for that pipeline if you want to use more. So it's a way for them to monetize and also to prevent abuse of their platform.
So the rate limit that they've introduced is 100 pools for every 6 hours for unauthenticated users.So an unauthenticated user is just a user that is pulling a Docker image from Docker Hub that hasn't logged in with that Docker hub credentials.
If you do log in, then you get 200 pores for every 6 hours.
So it doubles the limit. And this should be more than enough to follow this course. So you shouldn't need to upgrade to a different plan. You should be able to manage, which is 200 pores for every 6 hours.In fact, both of these right limits would normally be fine for a project like this. However, the problem is that we're going to be running Docker on GitHub actions, which is a shared service, so we're not going to be the only developers in the world using GitHub actions.
GitHub actions works by running our code on shared servers, which are used by many other projects and many other developers.
So this means that this hundred pools for every 6 hours is applied for every single person using the servers that are shared between all of the different developers on GitHub actions. This is a problem because this means that there's 100 pools every 6 hours gets quickly used up. So the way that we're going to get around this problem is we're going to authenticate with Docker Hub.So to authenticate with Docker Hub will start by creating a Docker Hub account. Then we're going to set up credentials that are used by our project in order to log in before we run a job that pools docker images. This means we can take advantage of the 200 pools for every 6 hours, which should be more than enough to follow this course.

so basically docker reduces the process of manully installing dependencies, source code and running application on server

So how do you configure Docker to work with Django?
So we start by defining a Docker file that has all of the operating system level dependencies needed
for our project. Docker follow is simply just a list of steps that Docker uses to create an image for our project.
You start by choosing the base image because we were going to be building a Python project. We're going to use the Python base image that is provided for free on Docker hub.
Then we install dependencies in our image. So these are operating system level dependencies and I'll show you what I mean by that as we get to
that part of the course, you then set up users. So these are the Linux users that are needed to run our application and these users are created inside
our Docker container.


We're also going to set up Docker compose for our project.
Docker composed defines how Docker images should be used to run out development server.
You basically define the images as different services and every service has a name.
For example, we're going to be using the name app.
You can define various port mappings which make ports accessible on your local machine, and this is
how we're going to actually connect to the containers that are running our application.
And you can set up volume mappings. Volume mappings is important because it's how the code in our project gets into the Docker container.
Once you've set all of this up, we're going to be using Docker Compose as follows.
So we're going to run all of the commands through Docker Compose, and the commands are going to look like this.
Here's an example of running the collect static Django command through Docker Compose.

docker-compose run --rm app sh-c "python manage.py collectstatic"

You start by typing docker hyphen compose which will run the Docker Compose application.
Then you pass in the run command which says that we wish to run a container and a single command on that container.
Then you specify this hyphen, hyphen, ram. This is optional.
However, it tells Docker Compose to remove the container.
Once it's finished running, it's recommended that you add this any time you're running a single command
because that means you don't have a build up of lingering containers on your system.
Then you specify the name of the app that you defined inside your Docker compose configuration.
The app that we're going to be using is going to be called App. Then you pass in S-H hyphen C.
so this is the command that is going to be passed into the container when it runs.
This command basically says We want to run a single command on our container.
Finally you pass in the Django command that you want to run inside quotations.
So in this particular example we're running Python managed API collect static, which is the Django
command for collecting static files. So the first part of this is the Docker compose syntax.
That's everything up until the app here. And this is basically the part that we need to add before every command that we run.
Then the second part of this is the command that is actually going to be run on the container. We always start with S-H height and see if we're going to be running a single command in the container
just so we can wrap our command in quotes and easily understand which part of the command is going to be running in the container.
So that's an overview of how we're going to be using Docker and Django together.


Git:
create a github project:
go to github -> create repository, add readme.md,mit license and also gitignore with python
now get the ssh clone url copy it
now in local machine:
>>>> git clone "url"
project gets clone to local machine

git stage changes
>>>git add .
git commit changes
>>>git commit -m "Added Github actions"
git push to origin
>>>>git push origin


superuser details:
sudhagadre@example.com
sudha123

other users:
user1@example.com
user123

cd_user_access_key_id = "AKIA2UC3AEBTWNHBSKNK"
cd_user_access_key_secret = <sensitive>

cd_user_access_key_id = "AKIA2UC3AEBTWNHBSKNK"
cd_user_access_key_secret = <sensitive>
ecr_repo_app = "730335289447.dkr.ecr.us-east-1.amazonaws.com/property-app-api-app"
ecr_repo_proxy = "730335289447.dkr.ecr.us-east-1.amazonaws.com/property-app-api-proxy"
