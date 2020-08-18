# API TaskTable

| [Русская версия](https://github.com/KonstErz/API_TaskTable/blob/master/README.ru.md) |

### This API is implemented using the Django tools, Django REST framework and Celery

---


# Database structure

The service database is represented by the following objects and models (http://localhost:1337/admin/)

## Application API Models

+ **TASK**
It has fields: 
*Name* - task name (this field is unique); 
*Specification* - detailed task description; 
*Due date* - task expiration date (deadline);
*Creator* - task creator (foreign key to the User model);
*Performer* - task performer (foreign key to the User model);
*Status* - current task status, provides a choice of three values: *n* - New, *w* - In work, *c* - Completed

+ **COMMENT**
It has fields: 
*Task* - the task to which the comment is directed (foreign key to the Task model); 
*Description* - comment text; 
*Author* - comment author (foreign key to the User model);
*Post date* - date of publication of the comment

## Authorization Tokens

+ **TOKENS**
It has fields: 
*Key* - user authorization token created when a new user is registered in the system; 
*User* - username (username user profile); 
*Created* - date and time of token creation (user registration in the system)

## Authentication and Authorization Data

+ **GROUPS** - groups of users

+ **USERS**
User profile has fields: 
*Username*; 
*Email Address*;
*First Name*; 
*Last Name*; 
*Staff Status* - defines user access rights in the system

## Celery results and Periodic tasks

Results of completed tasks Celery and data on periodic tasks Celery beat.

---


# The main functionality of the application API

The API provides 6 main functional modules, which can be accessed either through separate endpoints that support input in the *application/json* format, or through the *TaskViewSet* functionality, which supports both HTML form and raw data input.


1.	**REGISTRATION**

(http://localhost:1337/api/registration/)

Creates a new user in the system, a user authorization token in the system.
Returns the authorization token of the new user.

***Sample input content:***     `{"username": "Peter", "email": "pparker62@gmail.com", "password": "secretpasswd951"}`

where are the fields: 
*username* - desired user profile name in the system; 
*email* - E-mail address;
*password* - password for user authorization in the system


2.	**LOGIN**

(http://localhost:1337/api/login/)

Authenticates the user in the system, logs the user into his profile, provides rights to conduct other operations in the system. 
Returns the user id or error with status code 400 in case of authentication failure.

***Sample input content:***     `{"username": "Peter", "password": "secretpasswd951"}`

where are the fields: 
*username* - user profile name in the system; 
*password* - password for user authorization in the system


3.	**LOGOUT**

(http://localhost:1337/api/logout/)

POST request to this address will lead to user logout.


4.	**TASK CREATION**

(http://localhost:1337/api/taskcreation/)

An authenticated user can create a new task. This user will be automatically identified as the creator of the task, the default status of the new task is "New". When creating a new task, its name must be unique.
Returns the id of the new task if the data is valid.

***Sample input content:*** 
`{"name": "NY is in danger!", "specification": "Venom is planning something terrible. Need to know about his plans as soon as possible.", "due_date": "2020-12-20", "performer": "Peter"}`


5.	**TASK UPDATE**

(http://localhost:1337/api/taskupdate/)

The function allows you to edit an existing task. Only authenticated creator and performer of the task have the right to edit it. Only the creator of the task can change the performer.
Returns a message about successful task update or a 403 error if the task performer tries to change himself.

***Sample input content:*** 
`{"task_id": 1, "name": "NY is in danger! Again...", "specification": "Venom is planning something terrible. Need to know about his plans as soon as possible.", "due_date": "2020-12-24", "performer": "Peter", "status": "w"}`

where is the field: 
*task_id* - the id of the task you want to edit


6.	**ADDING A COMMENT**

(http://localhost:1337/api/addcomment/)

It implements adding a comment to the specified task. Requesting user will be the author of the comment. Any authenticated users can comment on tasks.
Returns a message about the successful addition of a comment.

***Sample input content:*** 
`{"task_name": "NY is in danger! Again...", "description": "Well, I got faith in you, Peter. You can do it =*"}`

where is the field: 
*task_name* - the name of the task you want to comment on


## TaskViewSet


+ **API ROOT**

(http://localhost:1337/api/)

The default basic root view for DefaultRouter.


+ **TASK LIST**

(http://localhost:1337/api/tasks/)

It implements the display of the list of tasks. Tasks are displayed by pagination of 10 tasks on one page. Sort in descending order of due date. Each item displays information about the task model, including information about task users (creator and performer) and URL address to a page with more detailed information. Task List includes Search Filter by task name and performer name (*Filters* button in the upper right corner of the display). Only authenticated users have access to this and all subsequent pages. At the bottom of this page there is an HTML form (or raw data form), by filling out which you can send a POST request to the server to create a new task. Requesting user will be the creator of the task.


+ **TASK INSTANCE**

(http://localhost:1337/api/tasks/1/ , where *1* is the task identifier)

Implements the display of detailed information about the task, including information about task users (creator and performer) and all comments on it. Task comments are sorted in descending order of publication date and including detailed information about the author (user). You can add a new comment to the task using the *Add comment* option (in the *Extra Actions* tab in the upper right corner of the display). The creator and performer of the task can use the HTML form (or raw data form) at the bottom of this page to send a PUT request to the server and edit the task (only the creator of the task can change the performer).


+ **ADD COMMENT**

(http://localhost:1337/api/tasks/1/add_comment/ , where *1* is the task identifier)

Includes an HTML form (or raw data form) to add a new comment to the current task (POST request to the server). Requesting user will be the author of the comment. Any authenticated users can comment on tasks.


## Additional functionality of the application API


+ **Sending Email**

Celery tasks in this project are configured in such a way that they can send emails to creators and performers of tasks. An email is sent when a new task is created, a task is updated and a comment is added to a task. The email contains detailed and up-to-date information about the task with which the manipulations were carried out, or about the comment, if it was published.

***Attention!***
EmailBackend of this application connects to Google mail via SMTP. Therefore, to activate this option, in the project settings you need to specify the actual Email and Password to your Google account (see the *EMAIL_HOST_USER* and *EMAIL_HOST_PASSWORD* variables in the *env.prod.example* file), on behalf of which Django will send emails. You will also need to enable the ["Less secure apps"](https://myaccount.google.com/lesssecureapps) option in the "Security" tab in your Google account. In addition, you may need to follow the instructions at this [link](https://accounts.google.com/DisplayUnlockCaptcha). For these purposes, you can use both your personal Google account and a specially created fake account. But never share your personal passwords publicly! For more information, see [Gmail Help](https://support.google.com/mail/answer/7126229).

Celery will log a warning message in the event of problems sending emails. Check that you have correctly entered the data for your Google account and followed the above steps. Celery tries 3 times every 5 min to send a problem email.


+ **Upload**

(http://localhost:1337/upload/)

The *upload* app has a small function that you can use to upload your media. Use the *Browse* button on the form to select a file (image) from your local directories. Click *Submit* to upload the selected file to the server. Now the picture will be available at http://localhost:1337/mediafiles/image_file_name.

---

### Service Features


***Advantages***

+ All operations related to tasks can be carried out only by users who are authorized in the system;
+ Task editing operations can be performed only by the creator and performer of this task;
+ Handling most common errors related to incorrect data entry;
+ Automatic distribution of emails with information about changes in tasks. It is the responsibility of Celery tasks and queues in RabbitMQ, which reduces the load on the server and makes the entire service more fault-tolerant;
+ All project cache and sessions are stored in Redis.


***Flaws***
+ The list of tasks should display only those tasks that are associated with the current user;
+ The performer of the task must be able to change the performer. In this case, the task will have the "Delegated" flag;
+ Ideally, it should be possible to assign multiple performers to a task, not just one. Thus, the Tasks model will be able to have the "performers" field, which is a many-to-many link to the User models;
+ The functionality of the application is not covered by tests.
 
---


### Quick start guide for starting a service on your local computer

1. This project exists as a docker container, for its correct mounting and launch on your local computer you will need to install the current versions of the [Docker Engine](https://docs.docker.com/engine/install/) (ver. from *19.03.0* and higher). 
2. To build a Docker image, you need files with environment variables *env.prod* and *env.db*. So rename the files *env.prod.example* and *env.db.example* from the repository accordingly. These files contain variables for the correct operation of the project. The values for the production environment are configured, pay attention to the *EMAIL_HOST_USER* and *EMAIL_HOST_PASSWORD* if you want to test how sending email works (see the section *"Sending Email"*).
3. To mount the image and start the containers, from the project root folder, run the following command in the terminal:

    ```
    docker-compose -f docker-compose.prod.yml up -d --build
    ```

4. With the following command you can create a superuser:

    ```
    docker-compose -f docker-compose.prod.yml exec web python3 manage.py createsuperuser
    ```

5. The project uses a PostgreSQL database in a container. With the interactive psql terminal you can check if the databases and all relations were created successfully:
    
    docker-compose -f docker-compose.prod.yml exec db psql --username=tasktable --dbname=tasktable_prod
    
    tasktable_prod=# \l     # List of databases
    
    tasktable_prod=# \c tasktable_prod
    You are now connected to database "tasktable_prod" as user "tasktable".
    
    tasktable_prod=# \dt    # List of relations

    tasktable_prod=# \q    # Exiting psql

6. The project uses an Nginx server which acts as a reverse proxy for Gunicorn to handle client requests as well as serve up static and media files. Now you can go to the server http://localhost:1337/ in your browser to go to the Api Root of the project. Sign in under the credentials of the superuser you created (http://localhost:1337/admin/ or at http://localhost:1337/api/login/) and try to create several test objects of each type. You can create a new user (http://localhost:1337/api/registration/), tasks and comments to them using the functionality described in the section *"The main functionality of the application API"*. Also, you can go to http://localhost:5555/ to use the Flower Dashboard to monitor Celery tasks if you are using email sending.


Other useful commands that may come in handy when working with the docker container of the project:
    
    docker-compose -f docker-compose.prod.yml logs -f    # Logs of running services (Ctrl+C - exit)
    
    docker-compose -f docker-compose.prod.yml down -v   # Remove the volumes along with the containers
    
    docker images       # List all running images
    docker images -a    # List all images
    
    docker ps       # List all running containers
    docker ps -a    # List all containers
    
    docker stop $(docker ps -a -q)      # Stop all containers
    docker rm $(docker ps -a -q)     # Remove all containers

    docker rm <ID_or_Name>    # Removing a specific container by ID or name
    
    docker rmi $(docker images -f dangling=true -q)    # Remove all images not tagged
    
    docker rmi <Image_ID>    # Removing a specific image by ID
    
    docker rmi $(docker images -a -q)    # Remove all images
    
    docker rmi -f $(docker images -a -q)    # Forced removing of all images
    
