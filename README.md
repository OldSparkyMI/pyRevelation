# pyRevelation
pyRevelation is a password manager for the GNOME desktop, released under the GNU GPL license. It stores all your accounts and passwords in a single, secure place, and gives you access to it through a user-friendly graphical interface. It is the successor of Revelation ported to PyGObject

# System requirements
## Base development OS
Ubuntu 16.04.3 LTS
## Dependencies
### System packages
apt command:
```
sudo apt install python3.5-dev object-introspection libgirepository1.0-dev libcrack2-dev python-gconf gir1.2-gconf-2.0
```
#### Packages
- python3.5-dev
- object-introspection
- libgirepository1.0-dev
- libcrack2-dev
- python-gconf
- gir1.2-gconf-2.0
### Python 3.5 requirements
pip3 command
```
pip3 install pygobject
pip3 install cracklib
pip3 install gi
pip3 install gobject
pip3 install pycrypto
``` 
#### Packages
- PyGObject
- cracklib
- gi
- gobject
- pycrypto