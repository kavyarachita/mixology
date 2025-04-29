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

$(document).ready(function () {
    $('#activity-btn').click(function () {
        console.log("Activity button clicked!");
        var uid = $(this).data('uid');
        var url = $(this).data('url');
        // check if activity widget already exists
        if ($('.activity-widget').length) {
            $('.activity-widget').remove();
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
                'user_only': 'false',
            },
        })
        .done(function (response) {
            var activityList = response.actions;
            console.log(activityList);
            var activityWidget = $('<div class="activity-widget"><button class="btn btn-warn close">Close</button></div>');
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
            
            $('.activity-widget .close').click(function () {
                $(this).parent().remove();
            });

        })
        .fail(function (xhr, status, error) {
            console.log("AJAX request failed: " + error);
        });

    });
});