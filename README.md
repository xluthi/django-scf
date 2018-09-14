django-scf
==========

django-scf est une application web permettant de gérer une compétition amicale de blocs d'escalade (bloc session). Il est basé sur le [framework python django][djangoproject].

Durant une bloc session, chaque participant doit essayer de réussir un certain nombre de blocs (30), avec un nombre non limité d'essai.  Le juge ne retient que le meilleur résultat pour chaque bloc: top, zone, ou rien du tout.

Les classements finaux sont établis par catégorie.  Pour chaque classement, chaque bloc a une valeur "TOP" (ex: 1000) à répartir équitablement entre tous les participants ayant réussi ce bloc, et une valeur "ZONE" (ex: 500) à répartir équitablement entre tous les participants ayant maitrisé la zone (donc y compris ceux qui ont toppé).

Les catégories, le nombre de blocs et les valeurs de chaque blocs sont configurables dans l'application.

[djangoproject]:https://www.djangoproject.com/

Installation sur une machine de dévelopement Windows
-----------------------------------------------------

Sous Windows, il faut d'abord installer python 3 et pip (inclus dans l'installateur python).

Pour mieux gérer les dépendances, le mieux est de créer un environnement virtuel python:

```
C:\>pip install virtualenv
C:\>python -m venv scf-ve
C:\>scf-ve\Scripts\activate.bat
(scf-ve) C:\>pip install django~=2.1.1
(scf-ve> C:\>git clone git@git.luthi.be:xavier/django-scf.git
```
Django est installé dans un environnement virtuel, qui sera similaire sur le serveur de production.

PS: [une très bonne explication pédagogique se trouve sur le site djangogirls][djangogirls virtualenv].

Ensuite, il faut modifier le ficher `stone\settings.py` pour activer les traces de debug et autoriser l'hôte local. Les lignes à modifier doivent ressembler à ceci:
```python
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']
```

Enfin, on lance le serveur de dévelopement avec la commande:
```
(scf-ve) C:\django-scf>python manage.py runserver
```
Si tout se passe bien, le site est accessible via [http://127.0.0.1:8000](http://127.0.0.1:8000).

[djangogirls virtualenv]:https://tutorial.djangogirls.org/fr/django_installation/#lenvironnement-virtuel


Déployer en production
----------------------

Les instructions suivantes sont pour un déployement en production sur un serveur Linux Debian avec Apache.

Premièrement, il faut cloner le dépôt git dans `/var/www/`.  Pour ne pas avoir de problème de droits d'accès UNIX, j'ai ajouté mon utilisateur dans le groupe `www-data`, et j'ai ajouté le bit "sticky" au répertoire adéquat:
```bash
cd /var
sudo chmod -R g+s www
cd www
git clone git@git.luthi.be:xavier/django-scf.git
```

Ensuite, il faut installer le module WSGI pour Apache et créer un VirtualHost dédié:
```bash
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo apt-get install python3-venv
```

En supposant un accès via HTTPS uniquement, le fichier `/etc/apache2/sites-available/scf.conf` de définition du VirtualHost ressemblera à ceci:
```Apache
WSGIPythonPath /var/www/django-scf
WSGIPythonHome /var/www/scf-ve
<VirtualHost *:443>
        ServerName scf.example.com
        DocumentRoot /var/www/html

        WSGIScriptAlias / /var/www/django-scf/stone/wsgi.py

        <Directory /var/www/django-scf/stone>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        Alias /static/ /var/www/django-scf/static/
        <Directory /var/www/django-scf/static/>
                Require all granted
                Options -Indexes
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/scf-error.log
        CustomLog ${APACHE_LOG_DIR}/scf-access.log combined

        SSLCertificateFile    /etc/ssl/certs/ssl-cert-snakeoil.pem
        SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
</VirtualHost>
```

Pour servir les fichiers statiques, il faut demander au module `staticfiles` de collecter tous les fichiers nécessaires:
```bash
python3 manage.py collectstatic
```


Enfin, on active le site et on recharge la configuration Apache:
```
sudo a2ensite scf
sudo systemctl reload apache2
```

Si tout se passe bien (on croise les doigts), le site devrait être accessible via https://scf.example.com
