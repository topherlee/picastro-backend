# Team-Bravo-2023 Django-Rest-Backend

## Vision

 This is the current backend for Picastro, an image sharing mobile application for astrophotographers. This backend is written in Python, using both [Django](https://docs.djangoproject.com/en/4.1/) and [Django Rest Framework](https://www.django-rest-framework.org/) to facilitate it's functionalities.


## Requirements
<details>
<summary>more about the requirements</summary>

In order to run the backend server on your local machine, you need Python and its package installer [pip](https://pypi.org/project/pip/) installed. Furthermore, you need to be familiar with [Django](https://docs.djangoproject.com/en/4.1/) and [Django Rest Framework](https://www.django-rest-framework.org/).

Currently (during development phase), the backend uses a local SQLite Database, so you also need SQLite installed on your machine.

All libraries needed to build this application can be found in requirements.txt. In order to install them, run `pip install -r requirements.txt`.
</details>


## Building and Running the Application
<details>
<summary>more about building and running the application</summary>

### Prerequisites
 
- Clone the source code onto your local machine
- `cd` into the root project folder
- setup a virtual environment by running the following two commands: `python -m venv .venv` and `.venv/Scripts/activate.bat` (Windows cmd.exe) or `source .venv/bin/activate` (Linux and MacOS)
- Run `pip install -r requirements.txt` to install dependencies
- `python manage.py migrate` to make database migrations.
- Run `python manage.py data_parser` to populate your database with data from a json file.
- Run `python manage.py createsuperuser` to create a superuser (administrator) for your local backend installation. Set user name and password to whatever you like.
- Create a `.env` file in the root folder of this repo.
- Run the command `python3 -c 'import secrets; print(secrets.token_hex(100))'` in order to create a new secret key.
- Add `export SECRET_KEY='<your_secret_key>'` (Linux/Mac) or `SECRET_KEY='<your_secret_key>'` (Windows) to your .env file and save the file.
- Run `source .env` in your terminal (Linux/Mac) or un-comment the Windows-specific lines for setting the secret key in `settings.py`.


### Run the backend
- How to run the backend, depends on the mode (production or development) and the domain. `settings.py` contains the settings for both modes and domains. You just need to un-comment the desired settings and comment out the undesired ones.
- Since we still operate in development mode (even on AWS), we applied the following settings:
```
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.0.2.2','13.42.37.75']
```
- Execute `python manage.py runserver` to start your local development server
- Open your browser and navigate to the respective IP address of your domain (either [127.0.0.1:8000/admin](127.0.0.1:8000/admin) or [13.42.37.75/admin](13.42.37.75/admin), then login with the above account to see the admin panel.
</details>


## Structure of the Code/Application
<details>
<summary>more about the structure</summary>

The folder `./picastro_backend` is the main folder of this backend, containing for example `settings.py`, the main `urls.py` and so on.

Currently the backend has two apps, `picastro` and `picastro_web`. The picastro app contains the common models and the backend for the mobile application, while picastro_web represents the backend for the web application, but does not contain any own models.

The `./htmlcov` folder contains the report for test coverage (see Testing) and the `./media` folder is the place, where uploaded images, resized images or user profile images will be saved to.

And last, but not least, the `./templates` folder contains all web templates.
</details>

## Testing the Application
<details>
<summary>more about testing the application</summary>

Currently, there are only a few tests implemented and working. In order to run the tests, execute the following command: `python manage.py test`
</details>


## Team Members
 Who's working on this branch?
 * Christopher Lee
 * Steffen Atlas
 * Mohtalifa A Ema