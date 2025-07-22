#!/bin/sh

# Configuración de conexión a Consul
CONSUL_HOST=${CONSUL_HOST:-consul}
CONSUL_PORT=${CONSUL_PORT:-8500}

# Esperar a que Consul esté disponible
until curl -f "http://${CONSUL_HOST}:${CONSUL_PORT}/v1/status/leader" 2>/dev/null; do
  echo "Esperando a que Consul esté disponible..."
  sleep 5
done

# Obtener IP del contenedor
CONTAINER_IP=$(hostname -i)

# Registrar el servicio frontend
curl -X PUT \
  --data '{
    "ID": "'"${SERVICE_ID}"'",
    "Name": "'"${SERVICE_NAME}"'",
    "Address": "'"${CONTAINER_IP}"'",
    "Port": 80,
    "Check": {
      "HTTP": "http://'"${CONTAINER_IP}"'/",
      "Interval": "10s",
      "Timeout": "5s"
    },
    "Tags": ["web", "ui", "frontend"]
  }' \
  "http://${CONSUL_HOST}:${CONSUL_PORT}/v1/agent/service/register"

# Mantener el contenedor en ejecución
tail -f /dev/null