Step to use this simple ftp-server :

1./ Run make env (you have to install virtualenv to run it, If you don't have please do some below steps) :
    
    1.1 / apt-get install pip 
    
    1.1 / pip install virtualenv 

2./ After make env => cd to env directory  run 
    
    ./bin/ftp-server [some parameters] 
Using : 
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        adress for ftp server, default: 0.0.0.0:9100
  -u USER, --user USER  user for ftp server
  -p PASSWORD, --password PASSWORD
                        password for ftp server
  -d DIRECTORY, --directory DIRECTORY
                        home directory for ftp server,default: /tmp/

Simple example : ./bin/ftp-sever -u huy -p huy
=> Create ftp server: at ftp://huy:huy@0.0.0.0:9100/tmp/
