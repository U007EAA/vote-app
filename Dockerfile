# Prefer minimal base images  - use official python runtime base image
FROM python:3.12.0b4-alpine3.17

# create a new user
RUN adduser -D pyadmin

# setup app directory
WORKDIR /app

# copy source code
COPY . .

# Set ownership and permissions for the working directory
RUN chown -R pyadmin:pyadmin /app
RUN chmod -R 755 /app

# switch to new user
USER pyadmin

# install packages/dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 5000

# Instantiate/run the app
CMD ["python","app.py"]
