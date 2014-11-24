import json

from django.contrib.auth.decorators import permission_required

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow

from wagtail.wagtailembeds.models import Embed


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
