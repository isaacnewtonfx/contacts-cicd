Web Programming with Python and JavaScript

Project Author: Isaac Newton Kissiedu

This project is an online phonebook app powered by the Python Django Framework.

The project relies on HTML, CSS,Bootstrap Framework, Python, Django, sqlite for the data storage.

The project follows Agile Methodology using Docker, Travis-CI, CICD custom deploy to a dedicated VPS



**HOW TO RUN THE APP ON A VPS SERVER**

1. Setup nginx subdomain to reverse proxy /contacts to 

   ```
   #static uri location
    location /static_contacts/ {
        root /path/to/project/root folder/;
    }

    #reverse proxy pointing to the container port
    location /contacts {
        proxy_pass http://127.0.0.1:9001;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        client_max_body_size 100M;
        client_body_buffer_size 1m;
        proxy_intercept_errors on;
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 256 16k;
        proxy_busy_buffers_size 256k;
        proxy_temp_file_write_size 256k;
        proxy_max_temp_file_size 0;
        proxy_read_timeout 300;
        expires off;
   }
   ```


2. Install Docker Engine and Docker Compose on the server. Use the command `$ docker info` to check if docker is installed

3. CD into the project root directory

4. Run the command `$ docker-compose -f docker-compose-prod.yml up -d` to build and create the container

5. Open a web browser and visit ServerDomainName/contacts or SubDomainName/contacts



**HOW TO RUN THE APP ON LOCALHOST**

1. Install Docker Engine and Docker Compose on the local machine. Use the command `$ docker info` to check if docker is installed

2. CD into the project root directory

3. Run the command `$ docker-compose -f docker-compose-dev.yml up -d` to build and create the container

4. Open a web browser and visit localhost:9001/contacts