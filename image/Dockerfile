############################################################
# Dockerfile to build apache-flask container images
# Based on Ubuntu
############################################################

# Set the base image to the operation zombie base image
FROM operationzombie/base

# File Author / Maintainer
MAINTAINER Layne Small

# Create the default directory
RUN mkdir -p /srv/www
RUN mkdir -p /srv/scripts

ADD image_scripts/ /srv/scripts

# Clone the app from github and install packages
RUN git clone https://github.com/operationzombie/apache-flask.git /srv/www/app
RUN cp -f /srv/www/app/apache/config/default.conf /etc/apache2/sites-available/000-default.conf
RUN pip install -r /srv/www/app/requirements.txt 

##################### INSTALLATION END #####################

# Expose the default port
EXPOSE 80

# Set default container command
ENTRYPOINT /usr/sbin/apache2ctl -D FOREGROUND
