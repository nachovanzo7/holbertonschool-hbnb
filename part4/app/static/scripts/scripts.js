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
                  window.location.href = 'index.html'; // Redirige al usuario
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

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block'; // Mostrar el enlace de inicio de sesión
  } else {
      loginLink.style.display = 'none'; // Ocultar el enlace de inicio de sesión
      fetchPlaces(token); // Si el usuario está autenticado, obtener los lugares
  }
}

async function fetchPlaces(token) {
  try {
      const response = await fetch('https://api.example.com/places', {
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

document.addEventListener('DOMContentLoaded', checkAuthentication);
