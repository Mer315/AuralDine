# Use nginx to serve static files
FROM nginx:alpine

# Remove default nginx config
RUN rm -f /etc/nginx/conf.d/default.conf

# Copy custom nginx config for backend proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy frontend files
COPY . /usr/share/nginx/html

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
