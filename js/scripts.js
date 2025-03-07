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

            var followingLabel = document.querySelector('.following-label');
            if (followingLabel) {
                followingLabel.remove();
            }
        } else {
            var followers = parseInt($('#followers-stat').text());
            console.log(followers);
            $('#followers-stat').text(followers + 1);
            $('.follow-btn').text('Unfollow');
            $('.follow-btn').addClass('following');
            $('.alert').text('Followed successfully');
            $('.alert').show();

            var followingLabel = document.createElement('button');
            followingLabel.classList.add('btn', 'following-label');
            followingLabel.disabled = true;
            followingLabel.textContent = 'Following';
            
            $('.profile-info').append(followingLabel);
        }
    });

    checkQueryString();

    checkCommentString();
});

function checkCommentString() {
    var commentStr = window.location.search;
    // console.log(commentStr);
    var urlParams = new URLSearchParams(commentStr);
    var comment = urlParams.get('comment-input');

    if (comment === null) {
        // console.log('No comment found');
        return;
    } else if (comment === '') {
        // console.log('empty comment found');
        $('.alert').text('Please enter a comment');
        $('.alert').show();
        return
    }

    var commentInput = document.querySelector('.comment-input');
    $('#user-comment').text(comment);
    $('.comment-input').val('');
    $('.alert').text('Comment added successfully');
    $('.alert').show();
    $('.comment-output').show();
}


function checkQueryString() {
    var queryStr = window.location.search;
    // console.log(queryStr);
    var urlParams = new URLSearchParams(queryStr);
    var keywords = urlParams.get('query');

    if (keywords === null) {
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

function addIngridient() {
    var ingredientList = document.querySelector('#ingredients');
    var numOfIngredients = ingredientList.children.length;
    var newIngredient = document.createElement('li');
    var inputField = document.createElement('input');
    var removeBtn = document.createElement('button');

    inputField.type = 'text';
    inputField.name = 'ingridient-' + (numOfIngredients);
    inputField.required = true;

    removeBtn.type = 'button';
    removeBtn.textContent = 'Remove';
    removeBtn.classList.add('btn');

    removeBtn.addEventListener('click', removeIngredient (newIngredient));

    newIngredient.appendChild(inputField);
    newIngredient.appendChild(removeBtn);
    ingredientList.appendChild(newIngredient);
}

function removeIngredient(ingredient) {
    return function() {
        if (ingredient === null) {
            return;
        }
        ingredient.remove();
        // update ids of the remaining ingredients
        var ingredients = document.querySelectorAll('#ingredients li');
        var i = 0;
        ingredients.forEach(function(ing) {
            var inputField = ing.querySelector('input');
            inputField.name = 'ingridient-' + (i);
            i++;
        });
    }
}