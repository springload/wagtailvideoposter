import json

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailsearch.backends import get_search_backends

from wagtail.wagtailimages.models import get_image_model
from wagtail.wagtailimages.forms import get_image_form, ImageInsertionForm
from wagtail.wagtailimages.formats import get_image_format
from wagtail.wagtailimages.fields import MAX_UPLOAD_SIZE

from wagtail.wagtailembeds.models import Embed

from wagtailvideoposter.models import EmbedVideoPosterImage


def get_image_json(image):
    """
    helper function: given an image, return the json to pass back to the
    image chooser panel or the editor to set the poster image
    """
    format = get_image_format('left')
    preview_image = image.get_rendition(format.filter_spec)
    return json.dumps({
        'id': image.id,
        'title': image.title,
        'format': format.name,
        'alt': image.title,
        'class': format.classnames,
        'preview': {
            'url': preview_image.url,
            'width': preview_image.width,
            'height': preview_image.height,
        },
        'html': format.image_to_editor_html(image, image.title),
    })


@permission_required('wagtailadmin.access_admin')
def chooser(request):
    Image = get_image_model()

    if request.user.has_perm('wagtailimages.add_image'):
        ImageForm = get_image_form()
        uploadform = ImageForm()
    else:
        uploadform = None

    q = None
    if 'q' in request.GET or 'p' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            q = searchform.cleaned_data['q']

            # page number
            p = request.GET.get("p", 1)

            images = Image.search(q, results_per_page=10, page=p)

            is_searching = True

        else:
            images = Image.objects.order_by('-created_at')
            p = request.GET.get("p", 1)
            paginator = Paginator(images, 10)

            try:
                images = paginator.page(p)
            except PageNotAnInteger:
                images = paginator.page(1)
            except EmptyPage:
                images = paginator.page(paginator.num_pages)

            is_searching = False

        return render(request, "wagtailimages/chooser/results.html", {
            'images': images,
            'is_searching': is_searching,
            'query_string': q,
            'will_select_format': request.GET.get('select_format'),
            'embed_id': request.GET.get('embed_id'),
        })
    else:
        searchform = SearchForm()

        images = Image.objects.order_by('-created_at')
        p = request.GET.get("p", 1)
        paginator = Paginator(images, 10)

        try:
            images = paginator.page(p)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)
    return render_modal_workflow(request, 'wagtailimages/chooser/chooser.html', 'wagtailimages/chooser/chooser.js', {
        'images': images,
        'uploadform': uploadform,
        'searchform': searchform,
        'is_searching': False,
        'query_string': q,
        'will_select_format': request.GET.get('select_format'),
        'embed_id': request.GET.get('embed_id'),
        'popular_tags': Image.popular_tags(),
    })


@permission_required('wagtailadmin.access_admin')
def poster_image_chosen(request, image_id, embed_id):
    image = get_object_or_404(get_image_model(), id=image_id)
    image_json = get_image_json(image)
    embed = Embed.objects.get(id=embed_id)
    embed_image = EmbedVideoPosterImage(embed=embed, image=image)
    embed_image.save()
    return render_modal_workflow(
        request, None, 'wagtailimages/chooser/poster_image_chosen.js',
        {'image_json': image_json}
    )


@permission_required('wagtailimages.add_image')
def poster_image_upload(request, embed_id):
    Image = get_image_model()
    ImageForm = get_image_form()

    searchform = SearchForm()

    if request.POST:
        image = Image(uploaded_by_user=request.user)
        form = ImageForm(request.POST, request.FILES, instance=image)

        if form.is_valid():
            form.save()

            # Reindex the image to make sure all tags are indexed
            for backend in get_search_backends():
                backend.add(image)

            if request.GET.get('select_format'):
                form = ImageInsertionForm(initial={'alt_text': image.default_alt_text})
                return render_modal_workflow(
                    request, 'wagtailimages/chooser/select_format.html', 'wagtailimages/chooser/select_format.js',
                    {'image': image, 'form': form}
                )
            else:
                # not specifying a format; return the image details now
                embed = Embed.objects.get(id=embed_id)
                embed_image = EmbedVideoPosterImage(embed=embed, image=image)
                embed_image.save()
                image_json = get_image_json(image)
                return render_modal_workflow(
                    request, None, 'wagtailimages/chooser/poster_image_chosen.js',
                    {'image_json': image_json}
                )
    else:
        form = ImageForm()

    images = Image.objects.order_by('title')

    return render_modal_workflow(
        request, 'wagtailimages/chooser/chooser.html', 'wagtailimages/chooser/chooser.js', {
            'images': images,
            'uploadform': form,
            'searchform': searchform,
            'max_filesize': MAX_UPLOAD_SIZE,
            'embed_id': embed_id
        }
    )
