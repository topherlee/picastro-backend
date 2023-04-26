# Structure of the Picastro Django-Rest-Backend

[Back to README](README.md)

---

## General Structure of the backend

The folder `./picastro_backend` is the main folder of this backend, containing for example `settings.py`, the main `urls.py` and so on.

Currently the backend has two apps, `picastro` and `picastro_web`. The picastro app contains the common models and the backend for the mobile application, while picastro_web represents the backend for the web application, but does not contain any own models.

The `./media` folder is the place, where uploaded images, resized images or user profile images will be saved to.

And last, but not least, the `./templates` folder contains all web templates.

The database file `db.sqlite3` will be created in the root folder of this repository, same as the `./htmlcov` folder after running coverage (see Testing)

---
[Back to README](README.md)