function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
$(document).ready(function() {

    // Initialize the follow button


    $('#follow-btn').click(function() {
        var userId = $(this).data('follow-uid');
        var followUrl = $(this).data('follow-url');
        $.ajax({
            url: followUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            dataType: 'json',
            data: {
                'user_id': userId,
            },
        })
        .done(function(response) {
            if (response.success) {
                // update ui text with the new follow status
                $('#follow-btn')
                    .text(response.is_following ? 'Unfollow' : 'Follow')
                    .data('following', response.is_following)
                    .toggleClass('following', response.is_following);
                // update the follower count
                $('#followers-label').text(response.follower_count);
            } else {
                console.log("Error: " + response.error);
            }
        })
        .fail(function(xhr, status, error) {
            console.log("AJAX request failed: " + error);
        });
    });
});


