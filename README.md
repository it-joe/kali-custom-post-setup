# Kali Post Setup Script
Author: [it-joe](https://github.com/it-joe)

> Kali Linux 2016.2 post-installation script for configuring my preferred system state after a fresh install.
* Installs preferred packages
* Creates desktop computer icon as *Nautilus* does not nativly provide a corresponding option
* Sets tweaks and other configurations through *dconf*
* Creates system wide mount point for existing SMB share
* Replaces default DNS resolver `4.2.2.2` located in `/usr/lib/proxychains3/proxyresolv` with custom entry
* Sets up random MAC address with each system start
* Activates the Network-Manager for wired interfaces

## Prerequisites 
The prerequisites are needed for generating the ASCII welcome banner only.

* pyfiglet
  * Pure Python implementation of http://www.figlet.org
* termcolor
  * Helper functions for ANSI color formatting
* colorama
  * Multiplatform support (Windows)

To avoid installing these prerequisites, simpy remove `dependencies()` and `banner()` from the `main()` function.

## Usage

### `packages()`
To install your preferred set of packages just look for this function and modify the `check_call()` arguments correspondingly.
### `set_tweaks()`
To enhance or modify these settings you have to locate the appropriate *dconf* option and modify the `check_call()` arguments according to your needs.
### `mount_smbshare()`
#### Prerequisites 
SMB share and user with access permissions must exist on Windows host. 
#### Create mount point
Assign variable `mnt_point_path` to a path of your choice. Default is `mnt_point_path = '/media/share'`.
#### Create authentication file
To avoid writing the password to `/etc/fstab` in clear text a dedicated authentication file should be created.
Replace the placeholder elements (between arrow brackets) of list `args = ['username=<USER>', 'password=<PASSWORD>']` with credentials of the authorized user.
#### Add entry to /etc/fstab for static mount point
Change the placeholder elements (between arrow brackets) of list `args = ['# windows smb share', '//<COMPUTERNAME>/<SHARE> /media/share cifs credentials=/root/.smbcredentials auto 0 0']` for configuring the share.
### `replace_dnssvr()`
You can swap the default DNS resolver `4.2.2.2` for a different one (currently stored is `213.73.91.35`).
### `random_mac()`
Appends command `macchanger -r eth0` to `/etc/rc.local`. Replace `eth0` with another network adapter if needed.
### `activate_networkmngr()`
Remove this function from the `main()` function if you want to keep the *Network-Manager* disabled (default).