function addIngredient() {
    const ingredientList = document.querySelector('#ingredients');
    const newIngredient = document.createElement('li');

    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.name = 'ingredients[]';
    inputField.required = true;

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.textContent = 'Remove';
    removeBtn.classList.add('btn');
    removeBtn.addEventListener('click', removeIngredient(newIngredient));

    newIngredient.appendChild(inputField);
    newIngredient.appendChild(removeBtn);
    ingredientList.appendChild(newIngredient);
}

function removeIngredient(ingredient) {
    return function () {
        if (ingredient !== null) {
            ingredient.remove();
        }
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const ingredientList = document.querySelector('#ingredients');
    const removeButtons = ingredientList.querySelectorAll('button');

    removeButtons.forEach(button => {
        const li = button.parentElement;
        button.addEventListener('click', removeIngredient(li));
    });
});

function confirmDelete(event) {
    const confirmed = confirm("Are you sure you want to delete this drink?");
    if (!confirmed) {
        event.preventDefault(); 
    }
}