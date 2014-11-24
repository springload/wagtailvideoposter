from django.conf.urls import url

from wagtailvideoposter.views import remover


urlpatterns = [
    url(r'^remover/embed/$', remover.remove_embed, name='posterimage_remove_embed'),
]
