function(modal) {
    modal.respond('response', {{ response|safe }});
    modal.close();
}