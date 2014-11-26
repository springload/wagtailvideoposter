from wagtail.wagtailcore import hooks
from django.conf.urls import include, url
from wagtailvideoposter import images_urls, embeds_urls
from django.utils.html import format_html_join, format_html
from django.conf import settings
from django.core.urlresolvers import reverse


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        # url(r'^posterimages/', include(admin_urls)),
        url(r'^images/', include(images_urls)),
        url(r'^embeds/', include(embeds_urls)),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    """
    Add extra JS files to the admin
    """
    js_files = [
        'wagtailvideoposter/js/embed-editor.js',
    ]

    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>', ((settings.STATIC_URL, filename) for filename in js_files))

    js_includes = js_includes + format_html("""
            <script>
                window.removersUrls = [];
                window.removersUrls.embedsRemover = '{0}';
                window.removersUrls.posterimageRemover = '{1}';
            </script>
        """, reverse('posterimage_remove_embed'), reverse('posterimage_remove_poster')
    )

    return js_includes
