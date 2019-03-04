# Portaladmin REST API

## Usage

The API endpoints support both JSON and HTML.
The interface can be browsed, therefore.

There are GET and POST operations on /api/mdstatement/

## Implementation


The API is implemented using the Djange REST framework.

Files:

* serializer.py  maps python <-> JSON
* urls.py    routes /api/ to views registered for the API router
* views.py   defines the selection and order for the API results
* settings.py INSTALLED_APPS, REST_FRAMEWORK
