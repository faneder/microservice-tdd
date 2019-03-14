# Microservices Flask
## Docker
Take note of the Docker compose file version used - 3.4 . Keep in mind that this does not relate
directly to the version of Docker Compose installed - it simply specifies the file format that you want
to use.
Build the image:
`$ docker-compose -f docker-compose-dev.yml build`

This will take a few minutes the first time. Subsequent builds will be much faster since Docker caches
the results of the first build. Once the build is done, fire up the container:

`$ docker-compose -f docker-compose-dev.yml up -d`
The -d flag is used to run the containers in the background

##### volume
The volume is used to mount the code into the container. This is a must for a development
    environment in order to update the container whenever a change to the source code is made.
    Without this, you would have to re-build the image after each code change.
    volumes:
      - './services/users:/usr/src/app'
      
### requirement
  When requirement is changes, we need to re-build the images since requirements are installed at build time rather than run time
  `$ docker-compose -f docker-compose-dev.yml up -d --build`
  
  
 ## Testing
    # Run test
  `docker-compose -f docker-compose-dev.yml \
run users python manage.py test`