// En frontend/js/api.js
const getServiceUrl = async (serviceName) => {
  try {
    const response = await fetch(`http://consul:8500/v1/catalog/service/${serviceName}`);
    const [service] = await response.json();
    return `http://${service.ServiceAddress}:${service.ServicePort}`;
  } catch (error) {
    console.error(`Error obteniendo URL para ${serviceName}:`, error);
    // Fallback a URLs directas si Consul falla
    const fallbackUrls = {
      'auth-service': 'http://auth-service:5000',
      'package-service': 'http://package-service:5002',
      'booking-service': 'http://booking-service:5003'
    };
    return fallbackUrls[serviceName];
  }
};

// Uso en tus funciones
const loginUser = async (credentials) => {
  const authUrl = await getServiceUrl('auth-service');
  const response = await fetch(`${authUrl}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  return response.json();
};