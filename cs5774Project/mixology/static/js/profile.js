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

    // Initialize the tag buttons
    $('.tags-container .btn').click(function() {
        var tagName = $(this).text().toLowerCase();
        var username = $(this).data('username');
        var uid = $(this).data('uid');
        var url = '/profile/'+ username
        $.ajax({
            url: url,
            type: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            dataType: 'json',
            data: {
                'uid':uid,
                'filter': tagName,
            }
        })
        .done(function(response) {
            if (response.success) {
                // update the drink cards
                var html = '';
                response.drinks.forEach(function(drink) {
                    html += `
                        <div class="card" href="/drink/${drink.id}">
                            <img class="card-img" src="${drink.image_url}" alt="Drink Image" />
                            <div class="card-content">
                                <h2>${drink.name}</h2>
                                <div class="view-more">
                                    <a href="/drink/${drink.id}">
                                        View More &rarr;
                                    </a>
                                    <div>
                                        <p>${drink.last_updated}</p>
                                        {% if user.is_authenticated and drink.poster.user == user or user.is_authenticated and user.is_superuser %}
                                        <form action="/edit-drink/${drink.id}" method="get">
                                            <button type="submit">Edit</button>
                                        </form>
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });
                $('.cards-container').html(html);
            } else {
                console.log("Error: " + response.error);
            }
        })
        .fail(function(xhr, status, error) {
            console.log("AJAX request failed: " + error);
        });
    });
});