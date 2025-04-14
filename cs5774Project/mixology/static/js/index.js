const filterSelect = document.getElementById('filter-select');
filterSelect.addEventListener('change', () => {
  const filterValue = filterSelect.value;
  fetch('/filter', {
    method: 'GET',
    params: { filter: filterValue }
  })
  .then(response => response.json())
  .then(data => {
    const filterResults = document.getElementById('filter-results');
    filterResults.innerHTML = '';
    data.forEach(result => {
      const resultHTML = `<p>${result.name}</p>`;
      filterResults.insertAdjacentHTML('beforeend', resultHTML);
    });
  });
});