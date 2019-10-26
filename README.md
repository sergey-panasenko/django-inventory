Django Inventory
===============

Installation
------------
Clone the repo with `git clone https://github.com/sergey-panasenko/django-inventory-app`.

Run `pip install -r requirements.txt`. Run `python setup.py install`.

Add `'django-inventory-app'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'django-inventory-app',
        ...
    )

Add the following to your projects `urls.py` file, substituting `inventory` for whatever you want the quiz base url to be.

    urlpatterns = patterns('',
        ...
        path('^inventory/', include('django-inventory-app.urls')),
        ...
    )
