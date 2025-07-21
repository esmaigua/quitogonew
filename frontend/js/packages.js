const BASE_PACKAGE_URL = "http://localhost:5002";
const token = localStorage.getItem("token");

if (!token) window.location.href = "login.html";

document.addEventListener("DOMContentLoaded", () => {
  validateAdmin();
  loadPackages();
});

async function validateAdmin() {
  const res = await fetch("http://localhost:5000/me", {
    headers: { Authorization: `Bearer ${token}` }
  });
  const user = await res.json();
  if (!user.is_admin) {
    alert("No tienes permisos para acceder a esta página.");
    window.location.href = "dashboard.html";
  }
}

async function loadPackages() {
  try {
    const res = await fetch(`${BASE_PACKAGE_URL}/packages`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    let html = `
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
            <th>Días</th>
            <th>Ubicación</th>
            <th>Participantes</th>
            <th>Incluye</th>
            <th>Desde</th>
            <th>Hasta</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
    `;

    data.packages.forEach((p) => {
      window[`package_${p.id}`] = p; // Guardar en variable global
      html += `
        <tr>
          <td>${p.name}</td>
          <td>${p.description}</td>
          <td>$${p.price}</td>
          <td>${p.duration_days}</td>
          <td>${p.location}</td>
          <td>${p.max_participants}</td>
          <td>${(p.includes || []).join(", ")}</td>
          <td>${p.available_from || "-"}</td>
          <td>${p.available_to || "-"}</td>
          <td>
            <button class="btn btn-sm btn-primary me-1" onclick="showUpdateForm('${p.id}')">Editar</button>
            <button class="btn btn-sm btn-danger" onclick="deletePackage('${p.id}')">Eliminar</button>
          </td>
        </tr>
      `;
    });

    html += "</tbody></table>";
    document.getElementById("package-list").innerHTML = html;
  } catch (error) {
    showAlert(error.message, "danger");
  }
}

function showCreateForm() {
  document.getElementById("form-container").innerHTML = `
    <div class="card card-body shadow-sm">
      <h5>Nuevo Paquete</h5>
      <form onsubmit="createPackage(event)">
        ${packageFormFields()}
        <button type="submit" class="btn btn-success">Crear</button>
      </form>
    </div>
  `;
}

function showUpdateForm(id) {
  const p = window[`package_${id}`];
  document.getElementById("form-container").innerHTML = `
    <div class="card card-body shadow-sm">
      <h5>Editar Paquete</h5>
      <form onsubmit="updatePackage(event, '${id}')">
        ${packageFormFields(p)}
        <button type="submit" class="btn btn-primary">Actualizar</button>
      </form>
    </div>
  `;
}

function packageFormFields(p = {}) {
  return `
    <div class="row mb-3">
      <div class="col">
        <label>Nombre</label>
        <input class="form-control" name="name" required value="${p.name || ""}" />
      </div>
      <div class="col">
        <label>Ubicación</label>
        <input class="form-control" name="location" required value="${p.location || ""}" />
      </div>
    </div>
    <div class="mb-3">
      <label>Descripción</label>
      <textarea class="form-control" name="description" required>${p.description || ""}</textarea>
    </div>
    <div class="row mb-3">
      <div class="col">
        <label>Precio</label>
        <input class="form-control" name="price" type="number" min="0" step="0.01" required value="${p.price || ""}" />
      </div>
      <div class="col">
        <label>Días</label>
        <input class="form-control" name="duration_days" type="number" min="1" required value="${p.duration_days || ""}" />
      </div>
      <div class="col">
        <label>Participantes</label>
        <input class="form-control" name="max_participants" type="number" min="1" required value="${p.max_participants || ""}" />
      </div>
    </div>
    <div class="row mb-3">
      <div class="col">
        <label>Incluye (separado por comas)</label>
        <input class="form-control" name="includes" value="${(p.includes || []).join(", ")}" />
      </div>
      <div class="col">
        <label>Desde</label>
        <input class="form-control" name="available_from" type="date" value="${p.available_from || ""}" />
      </div>
      <div class="col">
        <label>Hasta</label>
        <input class="form-control" name="available_to" type="date" value="${p.available_to || ""}" />
      </div>
    </div>
  `;
}

function getFormData(form) {
  const data = new FormData(form);
  const json = {};
  for (const [key, value] of data.entries()) {
    if (["price", "duration_days", "max_participants"].includes(key)) {
      json[key] = Number(value);
    } else if (key === "includes") {
      json[key] = value.split(",").map(i => i.trim()).filter(Boolean);
    } else {
      json[key] = value;
    }
  }
  return json;
}

async function createPackage(e) {
  e.preventDefault();
  const form = e.target;
  const body = getFormData(form);

  try {
    const res = await fetch(`${BASE_PACKAGE_URL}/packages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    showAlert("Paquete creado correctamente", "success");
    form.reset();
    loadPackages();
  } catch (error) {
    showAlert(error.message, "danger");
  }
}

async function updatePackage(e, id) {
  e.preventDefault();
  const form = e.target;
  const body = getFormData(form);

  try {
    const res = await fetch(`${BASE_PACKAGE_URL}/packages/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(body)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    showAlert("Paquete actualizado", "success");
    loadPackages();
    document.getElementById("form-container").innerHTML = "";
  } catch (error) {
    showAlert(error.message, "danger");
  }
}

async function deletePackage(id) {
  if (!confirm("¿Eliminar paquete definitivamente?")) return;
  try {
    const res = await fetch(`${BASE_PACKAGE_URL}/packages/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error);

    showAlert("Paquete eliminado", "success");
    loadPackages();
  } catch (error) {
    showAlert(error.message, "danger");
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
