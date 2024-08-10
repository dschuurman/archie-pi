# archie-pi

**ARCHIE** is an acronym for **A**nother **R**emote **C**ommunity **H**otspot for **I**nstruction 
and **E**ducation for use with the [Raspberry Pi](https://www.raspberrypi.org).

The ARCHIE Pi implements an offline web server that can be used to deliver educational content 
in remote locations where no internet access is available. Using a variety of open-source software 
(such as Linux, nginx, kiwix, and NetworkManager), this platform provides an "internet in a box" 
in the form of an open wi-fi access point that can be accessed by locally connected web browsers.
This access point uses a local web server to deliver educational content which may
include a wide variety of open educational resources like Wikipedia and Project Gutenberg.

The idea behind the ARCHIE Pi is not novel. The word *another* is included in the acronym to
acknowledge that it was inspired by other projects, such as the 
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

The ARCHIE Pi platform requires a recent version of Raspberry PI OS Lite (32-bit or 64-bit) 
and runs on any recent model of the Raspberry Pi that includes a builtin wifi adapter (including the latest Raspberry Pi 5).

A suitably sized microSD card is required, depending on the amount of content you want to install
(we have used 64GB, 128GB, and 256GB cards).
Note that not all microSD cards are created equal in terms of speed and reliability, so you may want to consult the 
[Raspberry Pi microSD guidelines](https://www.raspberrypi.org/documentation/installation/sd-cards.md).
It is recommended that you select a high-speed microSD card, such as cards rated for UHS Speed Class 3.
For the Raspberry Pi 5, it is recommend to use Class A2 compatible SD cards which include enhancements
such as command queueing of read/write requests.

Note that it is possible to use an external USB *drive* rather than a microSD card. 
For more information, consult the Raspberry Pi documentation describing 
[USB mass storage devices](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md).

During installation a separate wired Ethernet connection to the internet is temporarily required to download 
and install content for the ARCHIE Pi. The Wi-Fi connection is not available for internet access since it is 
configured as a stand-alone access point. If you don't have an Ethernet connection available, consider 
using another Raspberry Pi as a Wi-Fi to Ethernet bridge (tutorials are available online).
Once the installation is complete, the Ethernet connection will no longer be required.

## Installation instructions

Create a fresh image of the latest 
[Raspberry PI OS Lite](https://www.raspberrypi.org/software/operating-systems/)
on a suitably sized microSD card. Either 32-bit or 64-bit versions
of the OS can be used, but the 64-bit version is recommended if you
are using a Raspberry Pi model 3 B+ or newer model. We recommend the Lite version
of the Raspberry Pi OS since it requires less space on the SD card. 
Consult the Raspberry Pi documentation for 
[instructions](https://www.raspberrypi.org/software/) 
on how to install an image of the OS (using a handy tool called the
[Raspberry Pi Imager](https://www.raspberrypi.com/news/raspberry-pi-imager-imaging-utility/) is recommended).

Note that the installation requires an Ethernet connection during setup since the wifi adapter 
will be configured as an access point during the installation and therefore cannot be used as an
internet connection. Once the setup is complete, the ethernet connection is no longer required.

Plug in an ethernet cable with internet access and power up the Raspberry Pi.
Raspberry Pi OS Lite will perform an initial boot requiring you to configure a username, password, and
the keyboard settings. A typical default username for the Raspberry Pi is `pi` and you can select a 
suitable password (for security purposes, avoid using the default password of `raspberry`).

Next, install the `git` package as follows:
```
sudo apt update
sudo apt -y install git
```
With `git` installed, the latest revision of the `archie-pi` repository can 
be installed from the command line as follows:
```
git clone --depth 1 https://github.com/dschuurman/archie-pi.git
```
Once this repository is downloaded, enter the project folder as follows:
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
sudo ./setup.py --help
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
sudo ./setup.py --country US
```

Once the setup script has completed successfully, an open wi-fi access point should 
be advertised from the Raspberry Pi with an SSID of **ARCHIE-Pi** (unless a different SSID was selected 
using the `--ssid` command line argument). Using another device (such as a laptop or smartphone) connect 
to this access point. You should now be able to view the default ARCHIE Pi webpage by pointing your browser 
to the address: 
```
http://10.10.10.10
```
Note that you will still need to install content for the ARCHIE Pi, a process described in the section that follows.
> ***Note:***
> The `setup.py` script requires a fresh install of the Raspberry Pi OS.
> If the `setup.py` script fails for some reason you will need to correct the problem and start the installation again.
> It is recommended to use a fresh installation of Raspberry Pi OS when running the `setup.py` script.

### Installing and Removing Content on the ARCHIE Pi

Once the ARCHIE Pi is successfully installed, you are ready to add some web content. 
To add web content, another script is provided named `install-modules.py`.
This script provides a friendly interface from which you can select various 
Open Education Resources (OERs), like those available from [kiwix.org](https://www.kiwix.org/)
and [worldpossible.org](https://rachel.worldpossible.org/content), and install them on your ARCHIE Pi.

Before running the installer, ensure an ethernet cable is plugged in with access
to the internet and that you are in the `archie-pi` folder. 
Next, run the module installer as follows:
```
sudo ./install-modules.py
```
A menu will appear allowing you to select and install various modules. 
The installer will allow you to select multiple modules at once by pressing
the key association with each module. Depending on size of the modules selected and your internet speed, 
the installation may take a *long* time to complete and may be left unattended during the install.
Once the script completes, the new content should be visible at: `http://10.10.10.10`.

Note that some content requires substantial storage space,
so it is important to ensure that you select an adequately sized microSD card (or USB drive).

Another script is included module removal. To remove a module, type:
```
sudo ./remove-modules.py
```
An enumerated list of all installed modules will appear. Note that it may take a few moments for the complete
list to appear since the file storage size is computed as the the list is sequentially displayed.
Enter the number corresponding to the module you wish to remove and it will be removed.
Repeat to remove additional modules or type `q` to exit the script.

## Final Steps

After the setup and installation scripts have run successfully,
the Ethernet cable is no longer needed and may be removed. 
At this point you should also reboot the Raspberry Pi so that the 
new configuration settings can take effect. This can
be accomplished by typing the following from the command line:
```
sudo reboot
```
The ACRHIE Pi can now be run *headless* without a screen, keyboard, or mouse
attached. After the Raspberry Pi reboots, ensure that the Wi-Fi access point is visible 
on a client computer and that you can connect.
If you are connecting from a smartphone, be sure to turn off your cellular data
access to ensure that all traffic is routed to the ARCHIE Pi.
Navigate a browser to the URL `http://10.10.10.10` and ensure that
you see the main webpage for the ARCHIE Pi. 
Confirm that you are able to access all the web content as expected.

---

## Installing Custom Content

While the `install-modules` provides a convenient way to add existing content, 
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
The ARCHIE Pi runs a [kiwix server](https://wiki.kiwix.org/wiki/Kiwix-serve) on port 81 and new ZIM
files can be included. It is recommended that new ZIM files should go in a subfolder of `/var/www/modules` 
along with an appropriate `index.htmlf` file. ZIM files should be added to the kiwix library using 
the `kiwix-manage` tool which can be found, along with the XML library file, in `/home/pi/kiwix`.
Note that some ZIM files are extremely large and so they should be chosen such that they fit the
memory limitations of the Raspberry Pi (since the SD card is mounted *read-only* there
is no swap space, thus programs must fit in the available RAM).

Once new content is installed, the ownership for all the web files and folders in `/var/www/modules` 
should be set as follows:
```
sudo chown -R www-data.www-data /var/www/modules
```
This may take a moment to complete. Once it is finished, the SD card root partition should be 
returned back to read-only mode by rebooting the ARCHIE Pi by typing:
```
sudo mount -o remount,ro /
```
Note that the `install-modules.py` script performs all of these steps automatically; 
these steps are only required when installing custom content.

### Changing the Country Code
At any point after the initial setup is complete, you can modify the Wi-Fi country code using 
the `set-country.py` utility as follows:
```
sudo ./set-country.py
```
