# Use an Nginx base image
FROM nginx:alpine

# Copy frontend files to the web root
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
