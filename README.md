# wagtailvideoposter

> Poster images for Wagtail Video Embeds

*Check out [Awesome Wagtail](https://github.com/springload/awesome-wagtail) for more awesome packages and resources from the Wagtail community.*

## Quickstart

```sh
pip install wagtailvideoposter [GITHUB SSH URI]
```

Add wagtailvideoposter to your settings.py in the INSTALLED_APPS section:

```python
...
    'modelcluster',
    'core',
    'wagtailvideoposter',
    'wagtail.contrib.wagtailsitemaps',
...
```

Run migrations:

```sh
./manage.py migrate wagtailvideoposter

```

Enjoy!
