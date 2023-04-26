# Testing the Picastro Django-Rest-Backend

[Back to README](README.md)

---

## Packages used for testing

Currently, both the Django test suite, as well as the [pytest](https://pypi.org/project/pytest/) package are used for testing. It is suggested to remove one of those packages later on, to make maintenance easier.


## Coverage

To support our testing efforts, we use the Python package [coverage](https://pypi.org/project/coverage/)

The command `coverage html` produces a report in the `/htmlcov/index.html` file, which shows the current test coverage of the project. This report can also be used to get ideas on where tests are required. For more information, please check the documentation of this package.


## Location of the tests

The tests are located in a `/tests` folder inside of each app. The tests are separated into different files, depending on what is supposed to be tested. Thus, all tests related to views can be found in the `test_views.py` file. The `test_e2e.py` file contains all the end-to-end tests of the respective app.


## Running the tests

In order to run the tests, there are two options:
- `python manage.py test` runs the built-in Django test suite
- `pytest` runs pytest

However, both commands will execute the same tests.


## Future development

Anyone progressing with this development should at first extend the test coverage, as the current development team reached the point, where the low test coverage deemed it difficult to do the remaining tests manually.

Some tests are almost fully implemented, but need debugging. Information on the possible cause has been provided in the comments of the respective test.


## References

To implement the current tests, the following sources have been used:

- Django documentation
- Django Rest Framework documentation
- ['Django and DRF Testing Series'](https://www.youtube.com/watch?v=yaLXsADWfS4&list=PLP1DxoSC17LZTTzgfq0Dimkm6eWJQC9ki&index=12) by Kenyan Engineer
- ['API Testing Tutorial.'](https://www.youtube.com/watch?v=17KdirMbmHY&list=PLx-q4INfd95EsUuON1TIcjnFZSqUfMf7s&index=16) by Cryce Truly
- ['Django REST API UNIT Testing'](https://www.youtube.com/watch?v=z6_v1UQ9Ht0) by Stack{Dev}
- ['Django DRF eCommerce Project'](https://www.youtube.com/playlist?list=PLOLrQ9Pn6cawinBJbH5d9IfloO9RRPMiq) by Very Academy

---
[Back to README](README.md)