const BASE_PACKAGE_URL = "http://localhost:5002";
const BASE_BOOKING_URL = "http://localhost:5003";
const BASE_AUTH_URL = "http://localhost:5000";
const token = localStorage.getItem("token");

if (!token) window.location.href = "login.html";

document.addEventListener("DOMContentLoaded", () => {
  validateUser();
  loadPackages();
  loadBookings();
});

async function validateUser() {
  const res = await fetch(`${BASE_AUTH_URL}/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    alert("Token inválido o expirado");
    localStorage.removeItem("token");
    window.location.href = "login.html";
  }
}

function showAlert(msg, type = "info") {
  document.getElementById("alert-container").innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;
}

function loadPackages() {
  fetch(`${BASE_PACKAGE_URL}/packages`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(res => res.json())
    .then(data => {
      let html = `<h4>Paquetes Disponibles</h4><div class="row">`;
      data.packages.forEach(p => {
        html += `
          <div class="col-md-6">
            <div class="card mb-3 shadow-sm">
              <div class="card-body">
                <h5 class="card-title">${p.name}</h5>
                <p class="card-text">${p.description}</p>
                <p><strong>Precio:</strong> $${p.price} | <strong>Días:</strong> ${p.duration_days}</p>
                <form onsubmit="createBooking(event, '${p.id}')">
                  <label>Fecha de viaje:</label>
                  <input type="date" name="travel_date" class="form-control mb-2" required/>
                  <label>Participantes:</label>
                  <input type="number" name="participants" class="form-control mb-2" min="1" required value="1" />
                  <button type="submit" class="btn btn-sm btn-success">Reservar</button>
                </form>
              </div>
            </div>
          </div>`;
      });
      html += "</div>";
      document.getElementById("packages-container").innerHTML = html;
    })
    .catch(err => showAlert("Error cargando paquetes", "danger"));
}

async function createBooking(e, packageId) {
  e.preventDefault();
  const travel_date = e.target.travel_date.value;
  const participants = parseInt(e.target.participants.value);

  try {
    const res = await fetch(`${BASE_BOOKING_URL}/bookings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ package_id: packageId, travel_date, participants }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Error al reservar");

    showAlert("Reserva creada correctamente", "success");
    e.target.reset();
    loadBookings();
  } catch (err) {
    showAlert(err.message || "Error inesperado", "danger");
  }
}

function loadBookings() {
  fetch(`${BASE_BOOKING_URL}/bookings`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(res => res.json())
    .then(data => {
      let html = `<h4>Mis Reservas</h4>`;
      if (data.bookings.length === 0) {
        html += `<p>No tienes reservas aún.</p>`;
      } else {
        html += `<ul class="list-group">`;
        data.bookings.forEach(r => {
          const isCancelled = r.status === "cancelled";
          const itemClass = isCancelled ? 'text-muted text-decoration-line-through' : '';
          const badge = isCancelled ? `<span class="badge bg-secondary ms-2">Cancelada</span>` : '';
          const button = isCancelled
            ? ''
            : `<button class="btn btn-sm btn-danger" onclick="cancelBooking('${r.id}')">Cancelar</button>`;

          html += `
            <li class="list-group-item d-flex justify-content-between align-items-center ${itemClass}">
              <div>
                <strong>${r.package_name || r.package_id}</strong> - ${r.travel_date} (${r.participants} participantes)
                ${badge}
              </div>
              ${button}
            </li>
          `;
        });
        html += `</ul>`;
      }
      document.getElementById("bookings-container").innerHTML = html;
    })
    .catch(err => showAlert("Error cargando reservas", "danger"));
}

async function cancelBooking(id) {
  if (!confirm("¿Cancelar esta reserva?")) return;

  try {
    const res = await fetch(`${BASE_BOOKING_URL}/bookings/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Error al cancelar");

    showAlert("Reserva cancelada", "info");
    loadBookings();
  } catch (err) {
    showAlert(err.message || "Error inesperado", "danger");
  }
}
