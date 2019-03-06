# Portaladmin REST API

## Usage

The API endpoints support both JSON and HTML.
Documentation: http://localhost:8000/docs/

Examples with curl and coreapi:

    curl -X GET localhost:8000/api/mdstatement/
    curl -X GET localhost:8000/api/mdstatement/16/
    curl -X PATCH -d admin_note=1234 localhost:8000/api/mdstatement/16/
    
    # coreapi is included in the python virtualenv of PVZDweb 
    coreapi action mdstatement list
    coreapi action mdstatement read -p id=16
    coreapi action mdstatement partial_update -p id=16 -p admin_note=xyz
    

## Implementation


The API is implemented using the Djange REST framework.

Files:

* serializer.py  maps python <-> JSON
* urls.py    routes /api/ to views registered for the API router
* views.py   defines the selection and order for the API results
* settings.py INSTALLED_APPS, REST_FRAMEWORK


## Notes

There are 2 API endpoints for callback of the signature proxy. 
These are _not_ implemented with DRF, therefore not in that doc.
See pvzdweb/url.py and search SIGPROXYAPI 