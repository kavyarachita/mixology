const csrftoken = getCookie('csrftoken');


$(document).ready(function() {

    // check for confirmation before deleting the collection
    $('#delete-collection-btn').click(function() {
        var cid = $(this).data('cid');
        var url = $(this).data('url');
        var username = $(this).data('username');
        var confirmDelete = confirm("Are you sure you want to delete the collection?");
        if (confirmDelete) {
            $.ajax({
                url: url,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                dataType: 'json',
                data: {
                    'cid': cid,
                },
            })
            .done(function(response) {
                window.location.href = '/collections/' + username;
            })
            .fail(function(xhr, status, error) {
                console.log("AJAX request failed: " + error);
            });
        } else {
            console.log("Collection deletion cancelled.");
        }
    });

   // edit button will add remove buttons on all drinks
    $('#edit-btn').click(function() {
        var cid = $(this).data('cid');
         $('.card').each(function() {
            var card = $(this);
            // check if the card has a remove button
            if (!$(this).find('.remove-btn').length) {
                var viewMore = $(this).find('.view-more');
                viewMore.append('<button class="btn btn-warn remove-btn">Remove</button>');
                $(this).find('.remove-btn').click(function() {
                    var did = $(this).closest('.card').data('drink-id');
                    $.ajax({
                        url: '/delete-drink-from-collection/',
                        type: 'POST',
                        headers: {
                            'X-CSRFToken': csrftoken,
                            'X-Requested-With': 'XMLHttpRequest',
                        },
                        dataType: 'json',
                        data: {
                            'did': did,
                            'cid': cid,
                        },
                    })
                    .done(function(response) {
                        console.log(card);
                        card.remove();
                    })
                    .fail(function(xhr, status, error) {
                        console.log("AJAX request failed: " + error);
                    });
                });
            } else {
                $(this).find('.remove-btn').remove();
            }
        });
    });    
});