$(function() {

    // $('.richtext [contenteditable="false"]').each(function() {
    //     insertRichTextDeleteControl(this);
    // });

    $('.richtext [contenteditable="false"][data-type="video"]').each(function() {
        insertRichTextVideoEmbedImageControl(this);
    });

    $('.richtext [contenteditable="false"][data-type="video"][data-posterimage]').each(function() {
        insertRichTextVideoEmbedDeleteImageControl(this);
    });
    

});

// Set delete control for embeds which will actually remove the element from the DB. 
// On hold since the fact of removing it from the editor doesn't mean it would be removed from the RichTextField necessarily.
// function insertRichTextDeleteControl(elem) {
//     var a = $('<a class="icon icon-cross text-replace delete-control">Delete</a>');
//     $(elem).addClass('rich-text-deletable').prepend(a);
//     a.click(function() {
//         if ($(elem).hasClass("embed-placeholder") && $(elem).attr("data-type") === "video") {
//             var id = $(elem).attr("id");
//             return ModalWorkflow({
//                 url: window.removersUrls.embedsRemover + '?id=' + id,
//                 responses: {
//                     response: function(response) {
//                         if (response.status) {
//                             $(elem).fadeOut(function() {
//                                 $(elem).remove();
//                             });
//                         }
//                     }
//                 }
//             });
//         }
//         else {
//             $(elem).fadeOut(function() {
//                 $(elem).remove();
//             });
//         }
//     });
// }

// Set image icon to assign poster images to embed elements (only those whose type is Video)
function insertRichTextVideoEmbedImageControl(elem) {
    var a = $('<a class="icon icon-image text-replace posterimage-control">Set poster image</a>');
    $(elem).addClass('rich-text-editable').prepend(a);
    a.click(function() {
        var id = $(elem).attr("id");
        return ModalWorkflow({
            url: window.chooserUrls.imageChooser + '?embed_id=' + id,
            responses: {
                imageChosen: function(imageData) {
                    $($(elem).children("img").get(0)).attr("src", $(imageData.html).attr("src"));
                },
                newEmbed: function(embed) {
                    $(elem).attr("data-posterimage", embed);
                    insertRichTextVideoEmbedDeleteImageControl(elem);
                }
            }
        });
    });
}

// Set image icon to remove poster images from embed elements (only those whose type is Video)
function insertRichTextVideoEmbedDeleteImageControl(elem) {
    var a = $('<a class="icon icon-undo text-replace posterimage-delete-control">Remove poster image</a>');
    $(elem).addClass('rich-text-delete-editable').prepend(a);
    a.click(function() {
        var id = $(elem).attr("data-posterimage");
        return ModalWorkflow({
            url: window.removersUrls.posterimageRemover + '?id=' + id,
            responses: {
                deleted: function(response) {
                    // Set thumbnail url and remove icon
                    $($(elem).children("img").get(0)).attr("src", response.embed_thumbnail_url);
                    $(a).remove();
                }
            }
        });
    });
}
