# Installation
This tutorial was tested with Kali GNU/Linux rolling `2018.1`.

## Hardware
The PiRogue is based on:
*  a Raspberry Pi 3
*  a `TL WN725N` version `2.1` or `2.2` 
*  a 32GB SD-card
*  a `SSD1306` I2C 0.96" OLED screen

A custom 3D printed case is [available on Thingiverse](https://www.thingiverse.com/thing:2822262).

### Connect the OLED screen
To display things on the tiny screen, you have to connect it to the Rapberry Pi GPIO. Follow this wiring schema:
<p align="center">
  <img src="https://raw.githubusercontent.com/U039b/PiRogue/master/pictures/screen_wiring.png" alt="OLED screen wiring"/>
</p>

For more details about the screen and the GPIO, have a look to [my PiRouter tutorial](https://esther.codes/post/pi_router_story/#ep4).

## 1 - Install Kali GNU/Linux - _on your computer_
Please refer to the [Kali documentation](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi) for this step.

## 2 - Prepare the system - _on your PiRogue_
Connect your PiRogue to your ethernet network. An Internet connection is required. Once done, power it on and use `root` as username and `toor` as password to log in.
You need to get its IP address in order to install the customization. To do, open a terminal and type:
```
ifconfig eth0
```
and remember the IP address. It should look like `192.128.0.12`.

You also have to expand the root partition in order to get room: 
```
parted /dev/mmcblk0 resizepart 2 -- -1
resize2fs /dev/mmcblk0p2
```

Finally, take the time to upgrade your Linux distribution:
```
apt-get update
apt-get dist-upgrade
apt-get install sshpass
```

Generate SSH keys: 
```
rm /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
service ssh restart
```

Change the root password:
```
passwd root
```

## 3 - Install Ansible - _on your computer_
To install ansible, please follow the [Ansible documentation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

## 4 - Install PiRogue customization - _on your computer_
To install and configure your PiRogue, you have to clone the [PiRogue-ansible](https://github.com/PiRanhaLysis/PiRogue-ansible) Git repository:
```
git clone https://github.com/PiRanhaLysis/PiRogue-ansible.git /tmp/PiRogue
```

Then, go into the `/tmp/PiRogue` directory:
```
cd /tmp/PiRogue
```
and edit the `inventory.ini` file and correct the IP address specified just after `ansible_host=`. It should look like:
```
pirogue_1 ansible_host=192.128.0.12  ansible_ssh_user=root
```

**NB**: if you want to install the PiRogue customization on multiple PiRogue devices at the same time, just duplicate the configuration, one line per device. Be sure to specify the correct IP address for each device. Example:
```
pirogue_1 ansible_host=192.168.1.123  ansible_ssh_user=root
pirogue_2 ansible_host=192.168.1.124  ansible_ssh_user=root
pirogue_3 ansible_host=192.168.1.125  ansible_ssh_user=root
```

Finally, start the installation by using the following command:
```
ansible-playbook -i inventory.ini --ask-pass pirogue.yml
```
It will ask you an SSH password, use `toor` if you do not have changed your password on your PiRogue, otherwise, use your new password.

## 5 - Reboot - _on your PiRogue_
On you PiRogue, open a terminal and type the following command:
```
reboot
```
**NB**: Remember that all the PiRogue files reside in `/usr/share/PiRogue` on your PiRogue.

## 6 - Screen customization - _on your PiRogue_
PiRogue has a tiny OLED screen on top of it. This screen displays two different screens:
*  the boot screen defined in `oled-screen/boot.py`
*  the details screen defined in `oled-screen/infos.py`

## 7 - A little note about hostapd and WPA2

We use hostapd to create a new Wifi Access Point. This access point is protected using WPA2.

**some Wifi dongle does not support WPA2 when acting as an access point**. If you cannot connect to the PiRogue access point with the correct passphrase your Wifi dongle may not be supported.

We have successfully tested with:

* TP-Link WN722N v1
