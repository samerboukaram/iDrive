# Step 3: Download and Install Apache
sudo apt update
sudo apt install apache2
apache2 -version #check apache version

# Step 4: Configure Firewall
sudo ufw app list
sudo ufw allow ‘Apache’

# Step 5: Configure apache
sudo systemctl status apache2  #check if the apache service is running in green

# Step 6: Install and enable mod_wsgi
sudo apt-get install libapache2-mod-wsgi python-dev

# Step 7:  Creating folder for flask app, place the code files inside them
cd /var/www 
sudo mkdir webApp
cd webApp

# Step 8: Install flask
sudo apt-get install python-pip 
sudo pip install Flask 
sudo pip install flask_sqlalchemy

# Step 10: configure and enable virtual host
sudo nano /etc/apache2/sites-available/webApp.conf
    https://techwithtim.net/wp-content/up...  # CLICK TO DOWNLOAD THE CODE TO PUT IN webApp.conf
sudo a2ensite webApp 
systemctl reload apache2

# Step 11: Create .wsgi file
sudo nano webapp.wsgi 
    #Place the below code in the wsgi file
    """
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/webApp/")

    from webApp import app as application
    application.secret_key = 'Add your secret key'
    """

# Step 12: Restart apache
sudo service apache2 restart 
