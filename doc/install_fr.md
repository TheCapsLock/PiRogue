# Installation
Ce guide a été testé sur Kali GNU/Linux rolling `2018.1`.

## Hardware
Le PiRogue se base sur :
*  un Raspberry Pi 3
*  un dongle `TL WN725N` version `2.1` ou `2.2` 
*  une SD-card de 32GB
*  un écran OLED I2C de 0.96" `SSD1306`

Un boîtier réalisable avec une imprimante 3D est [disponible sur Thingiverse](https://www.thingiverse.com/thing:2822262).

### Connexion de l'écran OLED
Afin de tirer profit de l'écran, vous devez le connecter aux GPIO du Raspberry Pi en suivant ce schéma : 
<p align="center">
  <img src="https://raw.githubusercontent.com/U039b/PiRogue/master/pictures/screen_wiring.png" alt="OLED screen wiring"/>
</p>

Pour plus de détails, vous pouvez consulter le [tutoriel du PiRouter](https://esther.codes/post/pi_router_story/#ep4).

## 1 - Installer Kali GNU/Linux - _sur votre ordinateur_
Référez vous à la [documentation de Kali](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi) pour cette étape.

## 2 - Preparer le system - _sur votre PiRogue_
Connectez votre PiRogue en ethernet sur votre réseau local, une connection Internet est requise. Mettez votre PiRogue sous 
tension et utilisez le nom d'utilisateur `root` et la mot de passe `toor` pour vous connecter.

Pour installer la personnalisation, vous devez retenir l'adresse IP de l'interface `eth0`, celle connectée à votre réseau local.
```
ifconfig eth0
```

Afin de disposer de l'intégralité de la carte SD, il est nécessaire de redimensionner la partition principale :  
```
parted /dev/mmcblk0 resizepart 2 -- -1
resize2fs /dev/mmcblk0p2
```

C'est désormais le moment de mettre à jour votre distribution :
```
apt-get update
apt-get dist-upgrade
```

Il faut également regénérer les clefs SSH par défaut :
```
apt-get install sshpass
rm /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
service ssh restart
```

Et changer le mot de passe root :
```
passwd root
```

## 3 - Installer Ansible - _sur votre ordinateur_
Pour installer ansible, référez vous à la [documentation de Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

## 4 - Installer la personnalisation du PiRogue - _sur votre ordinateur_
Clonez le dépôt Git [PiRogue-ansible](https://github.com/PiRanhaLysis/PiRogue-ansible) :
```
git clone https://github.com/PiRanhaLysis/PiRogue-ansible.git /tmp/PiRogue
```

Ensuite, rendez-vous dans le dossier `/tmp/PiRogue` :
```
cd /tmp/PiRogue
```
et éditez le fichier `inventory.ini` afin de préciser l'adresse IP de votre PiRogue juste après `ansible_host=`. Cela devrait reseembler à :
```
pirogue_1 ansible_host=192.128.0.12  ansible_ssh_user=root
```

**NB** : si vous souhaitez installer la personnalisation sur plusieurs PiRogue, il est possible de le faire en une fois en ajoutant une ligne par PiRogue :
```
pirogue_1 ansible_host=192.168.1.123  ansible_ssh_user=root
pirogue_2 ansible_host=192.168.1.124  ansible_ssh_user=root
pirogue_3 ansible_host=192.168.1.125  ansible_ssh_user=root
```

Enfin, lancer l'installation avec la commande suivante :
```
ansible-playbook -i inventory.ini --ask-pass pirogue.yml
```
Le mot de passe de l'utilisateur `root` de votre PiRogue vous sera demandé au lancement de l'installation.

## 5 - Reboot - _sur votre PiRogue_
Il faut désormais redémarrer votre PiRogue en utilisant la commande :
```
reboot
```
**NB** : tous les fichiers de personnalisation sont stockés dans le dossier `/usr/share/PiRogue` sur votre PiRogue.

## 6 - Personnalisation de l'écran - _sur votre PiRogue_
Il est possible de modifier les informations affichées sur l'écran en éditant les fichiers suivants : 
*  l'écran de démarrage : `oled-screen/boot.py`
*  l'écran affichant les informations de connexion : `oled-screen/infos.py`

## 7 - Un petit mot sur hostapd et le WPA2

Nous utilisons hostapd pour créer un point d'accès Wifi. WPA2 est utilisé pour protéger l'accès à ce point d'accès.

**certaines clés Wifi (dongle) ne supportent pas WPA2 en mode point d'accès**. Si vous n'arrivez pas à vous connecter à votre point d'accès PiRogue avec le bon mot de passe, votre clé Wifi n'est peut être pas supportée.

Nous avons testé le matériel suivant avec succès :

* TP-Link WN722N v1
