document.getElementById('recommendation-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const genre = document.getElementById('genre').value;
    const max_runtime = document.getElementById('max_runtime').value;
    const streaming_services = document.getElementById('streaming_services').value.split(',');

    const requestData = {
        genre: genre,
        max_runtime: parseInt(max_runtime),
        streaming_services: streaming_services.map(service => service.trim())
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Debug print
        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = '';

        if (data.error) {
            recommendationsList.innerHTML = `<li>${data.error}</li>`;
        } else {
            data.forEach(movie => {
                const listItem = document.createElement('li');
                listItem.textContent = `${movie.title} - Rating: ${movie.user_rating} - Runtime: ${movie.runtime} minutes`;
                recommendationsList.appendChild(listItem);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});