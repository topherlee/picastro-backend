# Testing the Picastro Django-Rest-Backend

## Vision


## Packages used for testing

Currently, both the Django test suite, as well as the [pytest](https://pypi.org/project/pytest/) package are used for testing. It is suggested to remove one of those packages later on, to make maintenance easier.


## Coverage

To support our testing efforts, we use the Python package [coverage](https://pypi.org/project/coverage/)

`coverage run -m pytest`

The command `coverage html` produces a report in the `/htmlcov/index.html` file, which shows the current test coverage of the project. This report can also be used to get ideas on where tests are required. For more information, please check the documentation of this package.


## Location of the tests

The tests are located in a `/tests` folder inside of each app. The tests are separated into different files, depending on what is supposed to be tested. Thus, all tests related to views can be found in the `test_views.py` file. The `test_e2e.py` file contains all the end-to-end tests of the respective app.


## Running the tests

In order to run the tests, there are two options:
- `python manage.py test` runs the built-in Django test suite
- `pytest` runs pytest

However, both commands will execute the same tests.
