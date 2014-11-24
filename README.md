wagtailvideoposter
==================

Poster images for Wagtail Video Embeds

# Quickstart

``` $ pip install wagtailvideoposter [GITHUB SSH URI]```

add wagtailvideoposter to your settings.py in the INSTALLED_APPS section:

```
...
    'modelcluster',
    'core',
    'wagtailvideoposter',
    'wagtail.contrib.wagtailsitemaps',
...
```

Run migrations:

```
./manage.py migrate wagtailvideoposter

```

Enjoy!