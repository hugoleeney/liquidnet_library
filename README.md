# liquidnet exersize


## local installation

This project was built with Python 3.5.5. 

First you need to build an sqlite database. the easiest way to do this
is the following.

    $ pip install -r requirements
    $ python
    Python 3.5.5
    >>> from library import db
    >>> db.create_all()

To run the server in development run the following commands:

    $ pip install -r requirements  # if not done from above
    $ python run.py

To run the smoke test with the server running use the following command 
or something similar.

    PYTHONPATH=$PYTHONPATH:./ python library/test/smoke_test.py
     
To build the package run the following command.

    python setup.py sdist


## release & deployment

TBD

Dockerfile builds is untested.


## TODO

- configure 