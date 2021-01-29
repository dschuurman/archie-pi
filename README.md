# archie-pi

**ARCHIE** is an acronym for **A**nother **R**emote **C**ommunity **H**otspot for **I**nstruction 
and **E**ducation for use with the [Raspberry Pi](https://www.raspberrypi.org).

The ARCHIE Pi implements an offline web server that can be used to deliver educational content 
in remote locations where no internet access is available. Using a variety of open-source software 
(such as Linux, nginx, kiwix, and hostapd), this platform provides an "internet in a box" in the form of an
open wi-fi access point that can be accessed by locally connected web browsers.
This access point uses a local web server to deliver educational content which may
include a wide variety of open educational resources like Wikipedia and Project Gutenberg.

The idea behind the ARCHIE Pi is not novel. The word *another* is included in the acronym to
acknowledge that it was inspired by other projects, particularly the 
[RACHEL Pi](http://rachelfriends.org/rachel-pi-howto.html) project.

## Features

The ARCHIE Pi is compatible with the latest Raspberry Pi operating system and hardware versions.
This project includes a script to setup the ARCHIE Pi on a fresh image of Raspberry Pi OS Lite and
another script to install selected open education resources.

The ARCHIE Pi runs both a web server (nginx) for delivering general web content as well as a Kiwix 
server for delivering wiki content stored in [ZIM](https://wiki.openzim.org/wiki/OpenZIM) files.

The developers of this project were concerned about *robustness*. This is crucial since the ARCHIE Pi
is intended to be deployed in remote locations without ready access to replacement parts or IT support.
Of particular concern is the reliability of the microSD card under conditions
in which power may be suddenly lost. Sudden power loss *can* lead to SD card corruption if it
occurs during a write operation on the microSD card.
To address this, various adjustments are made to the system configuration to mount the 
microSD card in *read-only* mode, eliminating the possibility of any microSD card writes.
Consequently, the ARCHIE Pi does not require a formal shutdown procedure and may be simply
unplugged.

## Requirements

The ARCHIE Pi platform requires a recent version of Raspberry PI OS Lite 
and runs on any recent model of the Raspberry Pi (including the latest Raspberry Pi 4).

A suitably sized microSD card is required, depending on the amount of content you want to install
(we have used 64GB and 128GB cards).
Note that not all microSD cards are created equal in terms of speed and reliability, so you may want to consult the 
[Raspberry Pi microSD guidelines](https://www.raspberrypi.org/documentation/installation/sd-cards.md).
It is recommended that you select a high-speed microSD card, such as cards rated for UHS Speed Class 3.

Note that it is possible to use an external USB *drive* rather than a microSD card. 
For more information, consult the Raspberry Pi documentation describing 
[USB mass storage devices](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md).

## Installation instructions

Create a fresh image of the latest 
[Raspberry PI OS Lite](https://www.raspberrypi.org/software/operating-systems/)
on a suitably sized microSD card (consult the
Raspberry Pi documentation for 
[instructions](https://www.raspberrypi.org/software/) 
on how to install an image of the OS).

Plug in an ethernet cable connected to the internet and power up the Raspberry Pi.
The ethernet cable is necessary for internet access since the wireless interface 
will be configured during the installation as an open wi-fi access point.

Raspberry Pi OS Lite will boot into a terminal window with a login prompt. 
The default user is `pi` and the default password is `raspberry`. 
After logging into the Raspberry Pi, you may wish to
change the default password by typing:
```
passwd
```
This command will prompt you to set a new password.
It is recommended that you change the default password for security purposes.

Next, install the `git` package as follows:
```
sudo apt install git
```
With `git` installed, the latest revision of the `archie-pi` repository can 
be installed from the command line as follows:
```
git clone --depth 1 https://github.com/dschuurman/archie-pi.git
```
Once the repository is downloaded, enter the project folder as follows:
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

Next, run the setup script specifying the correct country code. The country code for the US is shown below, 
but it is your responsibility to substitute the correct country code for your region:
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

### Installing Content

Once the `setup.py` script is complete, you are ready to add some web content. 
To add content, another script is provided named `module-installer.py`.
This script provides a friendly interface from which you can select various 
Open Education Resources, like those available from [kiwix.org](https://www.kiwix.org/)
and [oer2go.org](http://oer2go.org/), and install them on your ARCHIE Pi.

Before running the installer, ensure an ethernet cable is plugged in with access
to the internet and that you are in the `archie-pi` folder. 
Next, run the module installer as follows:
```
sudo python3 module-installer.py
```
A menu will appear allowing you to select and install various modules. 
Once the script completes, the content should be displayed at: `http://10.10.10.10`
(note that some content may require a reboot before it appears - see the instructions given in the final steps).

The installation may take some time, depending in the size of the package(s)
and the speed of your connection. 
Note that some content requires substantial storage space,
so it is important to ensure that you select an adequately sized microSD card or
USB drive.

### Installing Custom Content

While the `module-installer` provides a convenient way to add existing content, 
you can also curate your own content and manually add it to your ARCHIE Pi. 
The content may include PHP code and any file formats viewable by a standard 
web browser (PDF, HTML, MP4, JPG, etc.). 
Before any content can be written (or any updates applied), the root partition 
on the SD card must first be changed from read-only mode to read-write mode as follows:
```
sudo mount -o remount,rw /
```
Web content should be placed in its own folder in the `/var/www/modules` folder 
with file ownerships set to the web server user (`www-data`).
A file named `index.htmlf` must be placed in the content folder which will be automatically 
imported and listed on the main page of the ARCHIE Pi. The content of the file should be 
nested within a `<div class="indexmodule">` tag which will apply the appropriate formatting
from an existing CSS file. The `index.htmlf` file should include the module name, 
an optional icon, and a short description of the module with hyperlinks to the content.

It is also possible to add content in the form of [ZIM](https://wiki.openzim.org/wiki/OpenZIM) files.
The ARCHIE Pi runs a [kiwix server](https://wiki.kiwix.org/wiki/Kiwix-serve) and new ZIM
files can be included. It is recommended that new ZIM files should go in a subfolder of `/var/www/modules` 
along with an appropriate `index.htmlf` file. ZIM files should be added to the kwiix library using 
the `kiwix-manage` tool which can be found, along with the XML library file, in `/home/pi/kiwix`.

Once new content is setup, the SD card root partition should be returned to read-only
mode by rebooting the ARCHIE Pi by or as follows:
```
sudo mount -o remount,ro /
```
### Final Steps

After the setup and installation scripts have run successfully,
the ethernet cable is no longer needed and may be removed. 
At this point you should also reboot the Raspberry Pi so that the 
new configuration settings can take effect. This can
be accomplished by typing the following from the command line:
```
sudo reboot
```
After the Raspberry Pi reboots, ensure that the wi-fi access point is visible 
and then confirm that you are able to access the web content as expected.
At this point, the ARCHIE Pi can run *headless*, without a monitor or
keyboard attached.