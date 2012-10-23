dtestproj
=========

A modified version of Zed Shaw's 'Gothons From Planet Percal' created to test out Django.


Usage
=====
-Presuming you're using Ubuntu
)Install Django
)Install django-model-utils:
apt-get install python-pip
pip install distribute
pip install --upgrade pip
NEW BASH WINDOW
pip install django-model-utils
sudo apt-get install libyaml-dev
sudo apt-get install python-dev
pip install pyyaml
)Create databases:
python manage.py syncdb
)Update settings.py: You'll need to modify NAME and point it to your sqlite db and fill in SECRET_KEY (Google: 'django generate SECRET_KEY')

Deployment:
See "Deploying static files in a nutshell" for the javascript & stylesheets in: 
https://docs.djangoproject.com/en/1.3/howto/static-files/
