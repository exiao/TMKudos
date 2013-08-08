TMKudos
=======

Kudos

Prerequisites
=============
- django >= 1.5.1
- python-mysqldb


Setup
=====
You can use the provided tmkudos.apache-vhosts.conf :
  sudo ln -s <path to your install/tmkudos.apache-vhosts.conf /etc/apache2/site-available/
  sudo a2ensite tmkudos.apache-vhosts.conf && service apache2 restart
