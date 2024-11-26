document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value; // Trae el email
            const password = document.getElementById('password').value; // Trae la contraseña

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST', // Usa POST
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password }) // Envía los datos como JSON
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`; // Guarda el token como cookie
                    window.location.href = 'home'; // Redirige al usuario
                } else {
                    alert('Login failed: ' + response.statusText); // Muestra un mensaje de error
                }
            } catch (error) {
                alert('An error occurred: ' + error.message); // Muestra errores de red
            }
        });
    }

    checkAuthentication();

    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(placeId);
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaces(data);
        } else {
            console.error('Error al obtener los lugares:', response.statusText);
        }
    } catch (error) {
        console.error('Error de red:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        console.warn('El elemento places-list no existe en esta página.');
        return;
    }
    placesList.innerHTML = ''; // Limpiar contenido previo

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place');
        placeDiv.setAttribute('data-id', place.id);

        placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description}</p>
            <p><strong>Ubicación:</strong> ${place.latitude} - ${place.longitude}</p>
            <p><strong>Precio:</strong> $${place.price}</p>
            <a href="places?placeId=${place.id}" class="details-button">View Details</a>
        `;

        placeDiv.setAttribute('data-price', place.price); // Atributo para facilitar el filtrado
        placesList.appendChild(placeDiv);
    });
}

const priceFilter = document.getElementById('price-filter');
if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const places = document.querySelectorAll('.place');

        places.forEach(place => {
            const placePrice = parseFloat(place.getAttribute('data-price'));
            if (selectedPrice === 'Todo' || placePrice <= parseFloat(selectedPrice)) {
                place.style.display = 'block'; // Mostrar el lugar
            } else {
                place.style.display = 'none'; // Ocultar el lugar
            }
        });
    });
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('placeId');
}

let token = null; // Variable para almacenar el token JWT

function checkAuthentication() {
    token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'block';
    }

    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces(token);
    }
}

async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: token ? {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            } : {}
        });

        if (response.ok) {
            const data = await response.json();
            displayPlaceDetails(data);
        } else {
            console.error('Failed to fetch place details');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) {
        console.warn('El elemento place-details no existe en esta página.');
        return;
    }
    placeDetails.innerHTML = ''; // Limpiar el contenido actual

    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-detail';

    // Crear contenido HTML para los detalles del lugar
    placeDiv.innerHTML = `
        <h2>${place.title}</h2>
        <p>${place.description}</p>
        <p><strong>Precio:</strong> $${place.price}</p>
        <p><strong>Amenidades:</strong> ${place.amenities && place.amenities.length > 0 ? place.amenities.map(amenity => amenity.name).join(', ') : 'No amenities listed'}</p>
        <h3>Reviews:</h3>
        <div id="reviews">
            ${place.reviews && place.reviews.length > 0 ? place.reviews.map(review => `
                <div class="review">
                    <p><strong>${review.user_id || 'Anonymous'}</strong> (${new Date(review.date_created).toLocaleDateString()}):</p>
                    <p>${review.text}</p>
                </div>
            `).join('') : '<p>No reviews yet.</p>'}
        </div>
    `;

    placeDetails.appendChild(placeDiv);
}
