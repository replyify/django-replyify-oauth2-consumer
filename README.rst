Official Django client for Replyify
===================================

A Django wrapper for Replyify's Python API bindings.

Installation
------------

You can install this package by using the pip tool and installing:

::

    $ pip install django-replyify-oauth2

Or:

::

    $ easy_install django-replyify-oauth2

Register Your Application with Replyify
---------------------------------------

-  Sign up for Replyify at https://app.replyify.com/access/signup

-  Register your application at
   https://app.replyify.com/oauth2/applications/register

   -  Supported OAuth2 configuration is Public / Authorization code.

Configure the django-replyify-oauth2 module
-------------------------------------------

From your previously configured app, found at https://app.replyify.com/oauth2/applications add the following to your Django settings:
- REPLYIFY_CLIENT_ID
- REPLYIFY_CLIENT_SECRET
- REPLYIFY_REDIRECT_URI
- REPLYIFY_USER_ID_FIELD

And add the following to your `urls.py`
::
	urlpatterns = patterns(
		...
		url(r'^replyify/', include('replyify_oauth2.urls', namespace='replyify')),
		...
	)


Using the Replyify API
----------------------

Documentation for the python bindings can be found here:

-  https://app.replyify.com/api/docs
-  http://replyify.com/api/docs/python

In the standard documentation (the first link), most of the reference
pages will have examples in Replyify's official bindings (including
Python). Just click on the Python tab to get the relevant documentation.

In the full API reference for python (the second link), the right half
of the page will provide example requests and responses for various API
calls.
