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

    $('#post-comment-btn').click(function() {
        var drinkURL = $(this).data('drink-url');
        var comment = $('#comment-text').val();
        var user_id =  $(this).data('user-id');
        var drink_id =  $(this).data('drink-id');
        $.ajax({
            url: drinkURL,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            dataType: 'json',
            data: {
                'user_id': user_id,
                'drink_id': drink_id,
                'comment': comment,
            },
        })
        .done(function(response) {
            if (response.success) {
                // update ui with the new comment
                reference_element = $('.drink-comments h2');
                console.log(reference_element);
                comment_element = document.createElement('div');
                comment_element.classList.add('comment')
                comment_element.innerHTML = `
                <div class="comment-header">
                    <a href="/profile/${response.username}">
                        <img src=${response.pfp_url} alt="User" class="icon" />
                        <p>${response.username}</p>
                    </a>
                    <p>${response.posted}</p>
                </div>
                <p id="user-comment">${response.comment}</p>
                `;
                console.log(comment_element);
                reference_element[0].insertAdjacentElement("afterend", comment_element);
            } else {
                console.log("Error: " + response.error);
            }
        })
        .fail(function(xhr, status, error) {
            console.log("AJAX request failed: " + error);
            console.log("AJAX request failed: " + xhr);
            console.log("AJAX request failed: " + status);
        });
    });
});


