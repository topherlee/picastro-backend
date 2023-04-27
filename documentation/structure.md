# Structure of the Picastro Django-Rest-Backend

[Back to README](../README.md)

---

## General Structure of the backend

The folder `./picastro_backend` is the main folder of this backend, containing for example `settings.py`, the main `urls.py` and so on.

Currently the backend has two apps, `picastro` and `picastro_web`. The picastro app contains the common models and the backend for the mobile application, while picastro_web represents the backend for the web application, but does not contain any own models.

The `./media` folder is the place, where uploaded images, resized images or user profile images will be saved to.

And last, but not least, the `./templates` folder contains all web templates.

The database file `db.sqlite3` will be created in the root folder of this repository. And at the moment, the static files of the picastro_web application are in the `/static` folder.

For further information, please check the [Django documentation](https://docs.djangoproject.com/).

## Picastro App

The backend of the mobile application is structured like a standard Django Rest Framework app. All required files are in the `/picastro` folder, except for the tests. They are located in `/picastro/tests` folder. For more information on testing this backend, please refer to [testing.md](testing.md).

## Picastro_web App

The backend of the web application is structured like a standard Django app. All required files are in the `/picastro_web` folder, except for the models, tests and static files. The tests are located in `/picastro_web/tests` folder. For more information on testing this backend, please refer to [testing.md](testing.md). The static files are currently in the `/static` folder, but should be moved inside the web application in the future.

As mentioned before, the web application uses the same models as the mobile application. Hence, it does not contain a separate models.py file, but imports the models from the mobile application backend.

---

[Back to README](../README.md)