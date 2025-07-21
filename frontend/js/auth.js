const BASE_AUTH_URL = "http://localhost:5000"; // Cambia por la IP o dominio en producción

// LOGIN
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      try {
        const response = await fetch(`${BASE_AUTH_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (!response.ok) {
          showAlert(data.error || "Error al iniciar sesión", "danger");
          return;
        }

        localStorage.setItem("token", data.token);

        const meRes = await fetch(`${BASE_AUTH_URL}/me`, {
          headers: { Authorization: `Bearer ${data.token}` }
        });

        const user = await meRes.json();
        if (!meRes.ok) {
          showAlert("Token inválido", "danger");
          return;
        }

        localStorage.setItem("user", JSON.stringify(user));
        window.location.href = "dashboard.html";
      } catch (error) {
        console.error(error);
        showAlert("Error de red al intentar iniciar sesión", "danger");
      }
    });
  }

  // REGISTER
  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const isAdmin = document.getElementById("isAdmin").checked;

      try {
        const response = await fetch(`${BASE_AUTH_URL}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, is_admin: isAdmin })
        });

        const data = await response.json();
        if (!response.ok) {
          showAlert(data.error || "Error al registrarse", "danger");
          return;
        }

        showAlert("Registro exitoso. Redirigiendo...", "success");
        setTimeout(() => window.location.href = "login.html", 2000);
      } catch (error) {
        console.error(error);
        showAlert("Error de red al registrarse", "danger");
      }
    });
  }
});

function showAlert(message, type = "info") {
  const container = document.getElementById("alert-container");
  container.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;
}
