import json

from django.contrib.auth.decorators import permission_required

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow

from wagtail.wagtailembeds.models import Embed

from wagtailvideoposter.models import EmbedVideoPosterImage


@permission_required('wagtailadmin.access_admin')
def remove_embed(request):
    if request.GET.get('id'):

        embed_id = request.GET.get('id')
        embed = Embed.objects.get(id=embed_id)
        embed.delete()
        return render_modal_workflow(
            request, None, 'wagtailvideoposter/remover/removed.js',
            {'response': json.dumps({'status': True})}
        )


@permission_required('wagtailadmin.access_admin')
def remove_posterimage(request):
    if request.GET.get('id'):

        posterimage_id = request.GET.get('id')
        posterimage = EmbedVideoPosterImage.objects.get(id=posterimage_id)
        embed = posterimage.embed
        posterimage.delete()
        return render_modal_workflow(
            request, None, 'wagtailvideoposter/remover/posterimage_removed.js',
            {'response': json.dumps({
                'status': True,
                'embed_id': embed.id,
                'embed_thumbnail_url': embed.thumbnail_url,
                'embed_title': embed.title
            })}
        )
