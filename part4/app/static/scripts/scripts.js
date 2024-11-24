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
  placesList.innerHTML = ''; // Limpiar contenido previo

  places.forEach(place => {
      const placeDiv = document.createElement('div');
      placeDiv.classList.add('place');
      placeDiv.setAttribute('data-id', place.id);

      placeDiv.innerHTML = `
          <h3>${place.name}</h3>
          <p>${place.description}</p>
          <p><strong>Ubicación:</strong> ${place.location}</p>
          <p><strong>Precio:</strong> $${place.price}</p>
      `;

      placeDiv.setAttribute('data-price', place.price); // Atributo para facilitar el filtrado
      placesList.appendChild(placeDiv);
  });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
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

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('placeId');
}

let token = null; // Variable to store the JWT token

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
        fetchPlaces(token);
    }
}


async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`https://http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers: token ? {
                'Authorization': 'Bearer ' + token
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
    placeDetails.innerHTML = ''; // Clear the current content

    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-detail';

    // Create HTML content for the place details
    placeDiv.innerHTML = `
        <h2>${place.name}</h2>
        <p>${place.description}</p>
        <p>Price: $${place.price}</p>
        <p>Amenities: ${place.amenities.join(', ')}</p>
        <h3>Reviews:</h3>
        <div id="reviews">
            ${place.reviews.length > 0 ? place.reviews.map(review => `
                <div class="review">
                    <p><strong>${review.user}</strong> (${review.date}):</p>
                    <p>${review.comment}</p>
                </div>
            `).join('') : '<p>No reviews yet.</p>'}
        </div>
    `;

    placeDetails.appendChild(placeDiv);
}

window.onload = function() {
    checkAuthentication();
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(placeId);
    } else {
        console.error('No place ID found in URL');
    }
};

document.addEventListener('DOMContentLoaded', checkAuthentication);