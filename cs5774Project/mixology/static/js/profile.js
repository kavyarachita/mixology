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

    $('#user-activity-btn').click(function () {
        var uid = $(this).data('uid');
        var url = $(this).data('url');
        // check if activity widget already exists
        if ($('.user-activity-widget').length) {
            $('.user-activity-widget').remove();
            return;
        }
        $.ajax({
            url: url,
            type: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
            dataType: 'json',
            data: {
                'uid': uid,
                'user_only': 'true',
            },
        })
        .done(function (response) {
            var activityList = response.actions;
            console.log(activityList);
            var activityWidget = $('<div class="user-activity-widget"><button class="btn btn-warn close">Cancel</button></div>');
            activityList.forEach(function (activity) {
                var activityItem = document.createElement('span');
                
                var subjectURL = document.createElement('a');
                subjectURL.href = activity.user.url;
                if (activity.user.username == response.username) {
                    subjectURL.innerHTML = "You";
                } else {
                    subjectURL.innerHTML = activity.user.username;
                }
               
                var object = document.createElement('a');
                if (activity.target && activity.target.url) {
                    object.href = activity.target.url;
                } else {
                    object.href = "#";
                }
                if (activity.target && activity.target.username) {
                    object.innerHTML += activity.target.username;
                } else if (activity.target && activity.target.drink) {
                    object.innerHTML += "on drink: " + activity.target.drink.name;
                }
                else if (activity.target && activity.target.name) {
                    object.innerHTML += activity.target.name;
                } else {
                    object.innerHTML += "Unknown target";
                }

                activityItem.innerHTML = `
                    ${subjectURL.outerHTML} ${activity.action_type} ${object.outerHTML} ${activity.timestamp}<hr>
                `;
                activityWidget.append(activityItem);
            });
            // append the widget to the body
            $('body').append(activityWidget);

            $('.user-activity-widget .close').click(function () {
                $(this).parent().remove();
            });
        })
        .fail(function (xhr, status, error) {
            console.log("AJAX request failed: " + error);
        });

    });
});