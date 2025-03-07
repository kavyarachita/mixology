$(document).ready(function() {
    $('.follow-btn').click(function() {
        if($(this).hasClass('following')) {
            var followers = parseInt($('#followers-stat').text());
            console.log(followers);
            $('#followers-stat').text(followers - 1);
            $('.follow-btn').text('Follow');
            $('.follow-btn').removeClass('following');
            $('.alert').text('Unfollowed successfully');
            $('.alert').show();
        } else {
            var followers = parseInt($('#followers-stat').text());
            console.log(followers);
            $('#followers-stat').text(followers + 1);
            $('.follow-btn').text('Following');
            $('.follow-btn').addClass('following');
            $('.alert').text('Followed successfully');
            $('.alert').show();
        }
    });

    $('.comment-btn').click(function() {
        var comment = $('.comment-input').val();
        $('#user-comment').text(comment);
        $('.comment-input').val('');
        $('.alert').text('Comment added successfully');
        $('.alert').show();
        $('.comment-output').show();
    });

    checkQueryString();
});

function checkQueryString() {
    var queryStr = window.location.search;
    console.log(queryStr);
    var urlParams = new URLSearchParams(queryStr);
    var keywords = urlParams.get('query');

    if (keywords === null) {
        // $('.alert').text('No query string found');
        return;
    } else if (keywords === '') {
        $('.alert').text('No search keywords found');
        $('.alert').show();
        return
    }
    
    var cards = document.querySelectorAll('.card');
    var i = 0;
    cards.forEach(function(card) {
        var title = card.querySelector('h2').textContent;

        if (title.toLowerCase().includes(keywords.toLowerCase())) {
            card.style.display = 'flex';
            i++;
        } else {
            card.style.display = 'none';
        }
    });

    if (i === 0) {
        $('.alert').text('No results found for : ' + keywords.toLowerCase());
        $('.alert').show();
    } else {
        $('.alert').text('Showing results for : ' + keywords.toLowerCase());
        $('.alert').show();
    }

}