from django.conf.urls import url

from wagtailvideoposter.views import chooser


urlpatterns = [
    url(r'^chooser/$', chooser.chooser, name='posterimage_chooser'),
    url(r'^chooser/(\d+)/(\d+)/$', chooser.poster_image_chosen, name='posterimage_poster_chosen'),
    url(r'^chooser/upload/(\d+)/$', chooser.poster_image_upload, name='posterimage_chooser_upload'),
]
