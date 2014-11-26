function(modal) {
    modal.respond('imageChosen', {{ image_json|safe }});
    modal.respond('newEmbed', {{ posterimage_id|safe }});
    modal.close();
}
