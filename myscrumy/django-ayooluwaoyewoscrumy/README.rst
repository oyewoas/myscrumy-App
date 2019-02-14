=====
ayooluwaoyewoscrumy
=====

ayooluwaoyewoscrumy is a simple Django app to conduct practical scrum processes. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "ayooluwaoyewoscrumy" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ayooluwaoyewoscrumy',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('ayooluwaoyewoscrumy/', include('ayooluwaoyewoscrumy.urls')),

3. Run `python manage.py migrate` to create the ayooluwaoyewoscrumy models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a scrum (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ayooluwaoyewoscrumy/ to participate in the scrum processes.