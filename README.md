# archie-pi

**ARCHIE** is an acronym for **A**nother **R**emote **C**ommunity **H**otspot for **I**nstruction 
and **E**ducation for use with the Raspberry **Pi**.

The ARCHIE Pi implements an offline web server that can be used to deliver enducational content 
in remote locations where no internet access is available. Using a variety of open-source software 
(such as Linux, nginx, and hostapd), this platform provides an "internet in a box" in the form of an
open wi-fi access point that can accessed by locally connected web browsers.
This access point runs a local web server which can be used to deliver educational content, 
including a wide variety of creative commons content such as Wikipedia and Project Gutenberg.

The idea behind the ARCHIE Pi is not novel. The word *another* is included in the acronym to
acknowledge that it was inspired by other projects, particularly the 
[RACHEL Pi](http://rachelfriends.org/rachel-pi-howto.html) project.

## Features

The ARCHIE Pi is compatible with the latest Raspberry Pi operating system and hardware versions.
This project includes a script to setup the ARCHIE Pi on a fresh image of Raspberry Pi OS Lite and
another script to install selected open education resources.

One of concerns of the developers of this project is *robustness*. This is crucial since the ARCHIE Pi
is typically deployed in remote locations without ready access to replacement parts or IT support.
Of particular concern is the reliability of the microSD card under conditions
in which power may be lost at any time. 
Sudden power loss can lead to SD card corruption if it
occurs during a write operation to the SD card.

For this reason, several measures are taken to reduce the frequency of microSD card writes.
*This work is ongoing, and ultimately the goal is to mount the microSD card in read-only mode
to eliminate the possibility of any microSD card writes.*

## Requirements

The ARCHIE Pi platform requires a recent version of 
Raspberry PI OS Lite and runs on any recent model of
the Raspberry Pi (including the latest Raspberry Pi 4).

Depending on the amount of content you want to install,
a suitably sized microSD card is required. 
Note that
not all microSD cards are created equal, so you may want to consult the 
[Raspberry Pi microSD guidelines](https://www.raspberrypi.org/documentation/installation/sd-cards.md).
It is recommended that you select a high-speed microSD card,
such as cards rated for UHS Speed Class 3.

Note that it is possible to use an external USB *drive* rather than a microSD card. 
For more information, see the Raspberry Pi documentation describing 
[USB mass storage devices](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md).

## Installation instructions

Create a fresh image of the latest 
[Raspberry PI OS Lite](https://www.raspberrypi.org/software/operating-systems/)
on a suitably sized microSD card (consult the
Raspberry Pi documentation for 
[instructions](https://www.raspberrypi.org/software/) 
on how to install an image of the OS).

Plug in an ethernet cable connected to the internet and power up the Raspberry Pi.
The ethernet cable is necessary since the installation script configures the 
wireless interface as an open wi-fi access point.

Raspberry Pi OS Lite boots to a terminal window
with a login prompt. 
The default user is `pi` and the default password
is `raspberry`. 
After logging into the Raspberry Pi, you may wish to
change the default password by typing:
```
passwd
```
This command will prompt you to set a new password.
It is recommended that you change the default
password for security purposes.

Next, install the `git` package and download the `archie-pi` repository to the Raspberry Pi. 
This can be done from the command line as follows:

```
sudo apt install git
git clone https://github.com/dschuurman/archie-pi.git
```
Once the repository to downloaded, enter the project folder as follows:
```
cd archie-pi
```
This folder contains two python scripts: one to setup the ARCHIE Pi platform
and another to install educational content.

The `setup.py` script must be run first. It recognizes several command line parameters, 
including a parameter to set the SSID of the access point and the
country code for the wi-fi interface.
To learn more about the command line parameters, type:
```
python3 setup.py --help
```
The only mandatory parameter is the `--country` parameter. 
This should be set to the country code corresponding
to the country where the ARCHIE Pi will be deployed. *This setting is essential to ensure
the access point complies with local wi-fi communications regulations and
frequency channels.* A list of standard two-letter country codes is available 
[here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

Next, run the setup script specifyig the correct country code. The country code for the US is shown below, 
but it is your responsibility to substitue the correct country code for your region:
```
sudo python3 setup.py --country US
```

Once the setup script has completed successfully, an open wi-fi access point should 
appear with an SSID of **ARCHIE-Pi** (unless a different SSID was selected using 
the `--ssid` command line argument). 

Once you connect to the access point, you can view the top-level ARCHIE Pi webpage 
by pointing a browser to the address: 
```
http://10.10.10.10
```

## Installing Content

Once the `setup.py` script is complete, you are ready to add some web content. 
To add content, another script is provided named `module-installer.py`.
This script provides a friendly interface from which you can select various 
Open Education Resources available from [oer2go.org](http://oer2go.org/) and
install them on your ARCHIE Pi.

To run the module installer, type:
```
sudo python3 module-installer.py
```
A menu will appear allowig you to select and install various modules. 
Once the script completes, the content should be displayed at: `http://10.10.10.10`.

At this point the ethernet cable is no longer needed and may be removed. 
Note that some content requires substantial storage space,
so it is important to ensure that you select an adequately sized microSD card or
USB drive.
