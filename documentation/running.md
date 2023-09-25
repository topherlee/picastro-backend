# Building and Running the Picastro Django-Rest-Backend

[Back to README](../README.md)

---

## Prerequisites
 
- Clone the source code onto your local machine
- `cd` into the root project folder
- setup a virtual environment by running the following two commands: `python -m venv .venv` and `.venv/Scripts/activate.bat` (Windows cmd.exe) or `source .venv/bin/activate` (Linux and MacOS)
- Run `pip install -r requirements.txt` to install dependencies
- Create a `.env` file in the root folder of this repo.
- Run the command `python3 -c 'import secrets; print(secrets.token_hex(100))'` in order to create a new secret key.
- Add `export SECRET_KEY='<your_secret_key>'` (Linux/Mac) or `SECRET_KEY='<your_secret_key>'` (Windows) to your .env file and save the file.
- Run `source .env` in your terminal (Linux/Mac) or un-comment the Windows-specific lines for setting the secret key in `settings.py`.
- Run `python manage.py migrate` to make database migrations.
- Run `python manage.py data_parser` to populate your database with data from a json file.
- Run `python manage.py createsuperuser` to create a superuser (administrator) for your local backend installation. Set user name and password to whatever you like.


## Running the backend
- How to run the backend, depends on the mode (production or development) and the domain. `settings.py` contains the settings for both modes and domains. You just need to un-comment the desired settings and comment out the undesired ones.
- Since we still operate in development mode (even on AWS), we used the following settings:
```
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.0.2.2','13.42.37.75']
```
- Execute `python manage.py runserver` to start your local development server
- Open your browser and navigate to the respective IP address of your domain (either [127.0.0.1:8000/admin](127.0.0.1:8000/admin) or [13.42.37.75/admin](13.42.37.75/admin), then login with the superuser account you created earlier to see the admin panel.


## Future development

Whenever a new package has been added to the application, execute `pip freeze > requirements.txt` to update the requirements.txt file.

Furthermore, after changes to the web application, the command `python manage.py collectstatic` needs to be executed, to make static files available in the deployed web application. At the moment, the static files of the web application are in the `/static` folder, and the `collectstatic` command will save them in the `/staticfiles` folder.


---
[Back to README](../README.md)