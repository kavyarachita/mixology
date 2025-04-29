
function edit_comment() {
  var commentRefElement = $(this).closest(".comment-header div");
  console.log(commentRefElement[0]);
  var editButton = $(this);
  var commentID = $(this).data("comment-id");
  var drinkURL = $(this).data("drink-url");
  var commentElement = $(this).closest(".comment").find(".user-comment");
  var commentText = commentElement.text();
  var inputField = $(
    '<textarea class="comment-textarea">{{ comment.text }}</textarea>'
  );
  inputField.val(commentText);
  var saveButton = $('<button class="btn btn-primary">Save</button>');
  saveButton.click(function () {
    var updatedComment = inputField.val();
    $.ajax({
      url: drinkURL,
      type: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      dataType: "json",
      data: {
        cid: commentID,
        comment: updatedComment,
      },
    })
      .done(function (response) {
        if (response.success) {
          commentElement.text(updatedComment);
          inputDiv.replaceWith(commentElement);
          commentRefElement[0].children[0].insertAdjacentElement(
            "afterend",
            editButton[0]
          );
        } else {
          console.log("Error: " + response.error);
        }
      })
      .fail(function (xhr, status, error) {
        console.log("AJAX request failed: " + error);
      });
  });
  var inputDiv = $('<div class="input-div"></div>');
  inputDiv.append(inputField);
  inputDiv.append(saveButton);
  commentElement.replaceWith(inputDiv);
  $(this).remove();
}

function delete_comment() {
  var commentID = $(this).data("comment-id");
  var drinkURL = $(this).data("drink-url");
  var commentElement = $(this).closest(".comment");
  $.ajax({
    url: drinkURL,
    type: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
      "X-Requested-With": "XMLHttpRequest",
    },
    dataType: "json",
    data: {
      cid: commentID,
    },
  })
    .done(function (response) {
      if (response.success) {
        commentElement.remove();
      } else {
        console.log("Error: " + response.error);
      }
    })
    .fail(function (xhr, status, error) {
      console.log("AJAX request failed: " + error);
    });
}

const csrftoken = getCookie("csrftoken");
$(document).ready(function () {
  // Attach event listeners to existing edit and delete buttons
  $(".drink-comments").on("click", "#edit-comment-btn", edit_comment);
  $(".drink-comments").on("click", "#delete-comment-btn", delete_comment);

  $("#post-comment-btn").click(function () {
    var drinkURL = $(this).data("drink-url");
    var comment = $("#comment-text").val();
    var user_id = $(this).data("user-id");
    var drink_id = $(this).data("drink-id");
    $.ajax({
      url: drinkURL,
      type: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      dataType: "json",
      data: {
        user_id: user_id,
        drink_id: drink_id,
        comment: comment,
      },
    })
      .done(function (response) {
        if (response.success) {
          // update ui with the new comment
          reference_element = $(".drink-comments h2");
          console.log(reference_element);
          comment_element = document.createElement("div");
          comment_element.classList.add("comment");
          comment_element.innerHTML = `
                <div class="comment-header">
                <div>
                    <a href="/profile/${response.username}">
                    <img src="${response.pfp_url}" alt="User" class="icon" />
                    <p>${response.username}</p>
                    </a>
                    <button class="btn" id="edit-comment-btn" data-comment-id="${response.cid}" data-drink-url="/edit-comment/">Edit</button>
                    <button class="btn btn-warn" id="delete-comment-btn" data-comment-id="${response.cid}" data-drink-url="/delete-comment/">Delete</button>
                </div>
                <p>${response.posted}</p>
                </div>
                <p class="user-comment">${response.comment}</p>
                `;
          // attach button listeners to the new comment
          var editButton = comment_element.querySelector("#edit-comment-btn");
          var deleteButton = comment_element.querySelector(
            "#delete-comment-btn"
          );
          editButton.addEventListener("click", edit_comment);
          deleteButton.addEventListener("click", delete_comment);
          console.log(comment_element);
          reference_element[0].insertAdjacentElement(
            "afterend",
            comment_element
          );
        } else {
          console.log("Error: " + response.error);
        }
      })
      .fail(function (xhr, status, error) {
        console.log("AJAX request failed: " + error);
        console.log("AJAX request failed: " + xhr);
        console.log("AJAX request failed: " + status);
      });
  });

  $("#collection-btn").click(function () {
    var getURL = $(this).data("url");
    var drink_id = $(this).data("drink-id");
    var uid = $(this).data("user-id");

    // Make the get request for the collections
    $.ajax({
      url: getURL,
      type: "GET",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      dataType: "json",
      data: {
        uid: uid,
        did: drink_id,
      },
    })
      .done(function (response) {
        //  make a modal to display collection choices
        var modal = document.createElement("div");
        modal.classList.add("modal");
        modal.innerHTML = `
            <div class="modal-content">
                <h2>Pick which collection(s) to save to</h2>
            </div>
            `;
        var modal_row = document.createElement("div");
        modal_row.classList.add("modal-row");
        modal_row.innerHTML = `
        <button class="btn btn-warn close">Cancel</button>
        `;
        // if no collections, prompt to create a new one
        if (response.collections.length == 0) {
            var prompt = document.createElement("p");
            prompt.textContent = "You have no collections. Create one to save this drink.";
            modal.querySelector(".modal-content").appendChild(prompt);
            var createButton = document.createElement("button");
            createButton.classList.add("btn", "btn-primary");
            createButton.innerHTML = "Create Collection";
            createButton.onclick = function () {
                window.location.href = "/collections/" + response.username;
            };
            modal_row.insertBefore(createButton, modal_row.firstChild);
            modal.querySelector(".modal-content").appendChild(modal_row);
        } else {
            var collectionList = document.createElement("div");
            collectionList.classList.add("collection-list");
            for (var i = 0; i < response.collections.length; i++) {
                var collection = document.createElement("div");
                collection.classList.add("collection");
                collection.innerHTML = `
                        <input type="checkbox" id="collection-${i}" value="${response.collections[i].id}">
                        <label for="collection-${i}">${response.collections[i].name}</label>
                        `;
                if (response.collections[i].drink_exists) {
                collection.querySelector("input").checked = true;
                }
                collectionList.appendChild(collection);
            }
            modal.querySelector(".modal-content").appendChild(collectionList);
            // add save button
            var saveButton = document.createElement("button");
            saveButton.classList.add("btn", "btn-primary");
            saveButton.id = "save-collection-btn";
            saveButton.innerHTML = "Save";
            modal_row.insertBefore(saveButton, modal_row.firstChild);
            modal.querySelector(".modal-content").appendChild(modal_row);
            var saveButton = modal.querySelector("#save-collection-btn");
            saveButton.onclick = function () {
                var collections_list = modal.querySelectorAll(".collection input");
                var selectedCollections = {};
                for (var i = 0; i < collections_list.length; i++) {
                selectedCollections[collections_list[i].value] =
                    collections_list[i].checked;
                }
                // save the drink to the collection(s)
                $.ajax({
                url: "/save-drink-to-collections/",
                type: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                dataType: "json",
                data: {
                    uid: uid,
                    did: drink_id,
                    collections: JSON.stringify(selectedCollections),
                },
                }).done(function (response) {
                    modal.remove();
                    $('.alert').append(`
                    <p class="success">Drink saved to collection(s)!</p>
                    `);
                })
                .fail(function (xhr, status, error) {
                    console.log("AJAX request failed: " + error);
                    console.log("AJAX request failed: " + xhr);
                    console.log("AJAX request failed: " + status);
                    console.log("Error: " + response.error);
                        $('.alert').append(`
                        <p class="error">Error: ${response.error}</p>
                        `);
                });
            };
        }
        document.body.appendChild(modal);
        var closeButton = modal.querySelector(".close");
        closeButton.onclick = function () {
          modal.remove();
        };
        window.onclick = function (event) {
          if (event.target == modal) {
            modal.remove();
          }
        };
      })
      .fail(function (xhr, status, error) {
        console.log("AJAX request failed: " + error);
        console.log("AJAX request failed: " + xhr);
        console.log("AJAX request failed: " + status);
      });
  });
});
