# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## Setting up a puzzle hunt
1. Deploy to heroku
2. Create an admin user for Django by logging into Heroku and opening bash.  Then run python manage.py createsuperuser.
3. Log into Django and create all the data:

## Creating the content
1. Create your segments - representing sets of clues in an area that's walking distance.
2. Create the clues for each segment.  Each clue can optionally have text and an image.  The order of clues is determined by the order_index field (lower indexes are presented first).  When uploading an image, it will be converted into base64 content in the content field automatically, so just upload an image and save it.  Each clue must also have a solution!
3. Create your segment orderings.  These give segments an order that they must be completed in a given puzzle.  For example, if a segment should show up as the 3rd segment in your puzzle, create a segment ordering for that segment with an index of "3".
4. Create your paths.  These are a set of segment orderings.