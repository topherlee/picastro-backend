# Team-Bravo-2023 Django-Rest-Backend

## Your next steps
* Change the .gitignore file to suite your needs - it's currently set to ignore python related temp files, etc. Google 'gitignore <your language>' to find examples.


## Vision
 Add something about what the application will do when more complete


## Requirements
In order to run the backend server on your local machine, you need Python and its package installer [pip](https://pypi.org/project/pip/) installed. Furthermore, you need to be familiar with [Django](https://docs.djangoproject.com/en/4.1/).

Currently (during development phase), the backend uses a local SQLite Database, so you need SQLite installed on your machine.

All libraries needed to build this application can be found in requirements.txt. In order to install them, run `pip install -r requirements.txt`.


## Testing the build
How do I test the code to ensure the build is correct?


## Building and Running the Application
 
- Clone the source code onto your local machine
- `cd` into the root project folder
- Run `pip install -r requirements.txt` to install dependencies
- `python manage.py migrate` to make database migrations.
- Run `python manage.py createsuperuser` to create a superuser (administrator) for your local backend installation. Set user name and password to whatever you like.
- Execute `python manage.py runserver` to start your local development server
- Open your browser and navigate to [127.0.0.1:8000/admin](127.0.0.1:8000/admin), then login with the above account to see the admin panel.

  
## Team Members
 Who's working on this branch?
 * Christopher Lee
 * Steffen Atlas
 * Mohtalifa A Ema