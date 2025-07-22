# Etapa de construcción
FROM node:18-alpine as builder

WORKDIR /app
COPY .. .  

# Etapa de producción
FROM nginx:alpine

# Copia los archivos estáticos a la raíz de Nginx
COPY --from=builder /app /usr/share/nginx/html

# Configuración de Nginx
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Script de registro en Consul
COPY docker/consul-register.sh /consul-register.sh
RUN chmod +x /consul-register.sh

EXPOSE 80

CMD ["sh", "-c", "/consul-register.sh & nginx -g 'daemon off;'"]