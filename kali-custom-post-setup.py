# !/usr/bin/env python
# ==============================================================================
# Title:           kali-custom-post-setup.py
# Version:         1.0
# Author:          it-joe (https://github.com/it-joe)
# DateCreated:     06/02/2017
# DateUpdated:     
# Python Version:  2.7.12+
# ==============================================================================

import sys
import os
import stat
import imp
import fileinput
from subprocess import STDOUT, check_call


def dependencies():
	"""Installs prerequisites needed for ASCII Art."""
	try:
		imp.find_module('pyfiglet')
	except ImportError:
		check_call(['pip', 'install', 'git+https://github.com/pwaller/pyfiglet'],
				   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	try:
		imp.find_module('termcolor')
	except ImportError:
		check_call(['pip', 'install', 'termcolor'],
				   stdout=open(os.devnull,'wb'), stderr=STDOUT)				   
	try:
		imp.find_module('colorama')
	except ImportError:
		check_call(['pip', 'install', 'colorama'],
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)	

			   
def banner():
	"""Creates welcome banner."""
	from colorama import init
	from termcolor import cprint
	from pyfiglet import figlet_format
	
	init(strip=not sys.stdout.isatty())  # Strip colors if stdout is redirected
	cprint(figlet_format('KaliCustomPostSetup', font='small'),
		   'green', attrs=['bold'])
	
	str_ver = 'kali-custom-post-setup.py v1.0'
	print str_ver.center(79) + "\n"

	
def packages():
	"""Installs preferred packages."""
	print "[*] Installing MultiTail..."
	check_call(['apt-get', 'install', '-y', 'multitail'],
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	print "[*] Installing Terminator..."
	check_call(['apt-get', 'install', '-y', 'terminator'],
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	print "[*] Installing cifs-utils..."
	check_call(['apt-get', 'install', '-y', 'cifs-utils'],
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	print "[*] Installing Tor..."
	check_call(['apt-get', 'install', '-y', 'tor'],
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)


def desktop_computer_icon():
	"""Creates desktop computer icon as Nautilus does not 
	nativly provide a corresponding option.
	"""
	print "[*] Creating 'Computer' desktop icon..."
	
	# Create computer desktop file
	desktop_filename = 'Computer.desktop'
	desktop_filepath = os.path.join('/root/Desktop', desktop_filename)
	args = ['[Desktop Entry]', 'Version=1.0', 'Type=Application', 'Terminal=false', 'Exec=nautilus /', 'Name=Computer', 'Icon=computer']
	with open(desktop_filepath, 'w') as f:
		f.writelines("%s\n" % l for l in args)
	
	# Desktop file must be executable
	os.chmod(desktop_filepath, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

	
def set_tweaks():
	"""Sets tweaks and other configurations through dconf."""
	print "[*] Setting some tweaks through dconf..."
	check_call('dconf write /org/gnome/nautilus/desktop/home-icon-visible true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/nautilus/desktop/network-icon-visible true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/nautilus/desktop/trash-icon-visible true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/nautilus/preferences/show-create-link true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/desktop/interface/clock-show-date true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/desktop/interface/clock-show-seconds true'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/desktop/screensaver/lock-enabled false'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('dconf write /org/gnome/nautilus/preferences/default-sort-order \'type\''.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)
	check_call('timedatectl set-timezone Europe/Berlin'.split(),
			   stdout=open(os.devnull,'wb'), stderr=STDOUT)

			   
def mount_smbshare():
	"""Creates system wide mount point for smb share.
	Available after restart.
	"""
	print "[*] Creating system wide mount point for existing smb share..."
	
	# Create mount point
	mnt_point_path = '/media/share'
	if not os.path.exists(mnt_point_path):
		os.makedirs(mnt_point_path)
	
	# Create authentication file
	cred_filename = '.' + 'smbcredentials'
	cred_filepath = os.path.join('/root', cred_filename)
	args = ['username=<USER>', 'password=<PASSWORD>']
	with open(cred_filepath, 'w') as f:
		f.writelines("%s\n" % l for l in args)
	
	# Add entry to /etc/fstab for static mount point 
	args = ['# windows smb share', '//<COMPUTERNAME>/<SHARE> /media/share cifs credentials=/root/.smbcredentials auto 0 0']
	lines = open('/etc/fstab', 'r').readlines()
	if not (lines[-2]).rstrip() == '# windows smb share':
		open('/etc/fstab', 'a').writelines("%s\n" % l for l in args)


def replace_dnssvr():
	"""Replaces default DNS resolver '4.2.2.2' with 
	'213.73.91.35' (dnscache.berlin.ccc.de).
	"""
	print "[*] Replacing the DNS Server '4.2.2.2' with '213.73.91.35'..."
	for line in fileinput.FileInput("/usr/lib/proxychains3/proxyresolv", inplace=1):
		print line.replace("4.2.2.2", "213.73.91.35").rstrip()

		
def random_mac():
	"""Sets up random MAC address with each system start."""
	print "[*] Setting up random MAC address..."
	file = "/etc/rc.local"
	
	# Read the file into a list of lines
	lines = open(file, 'r').readlines()

	# Edit the second last line of the list of lines
	if not (lines[-2]).rstrip() == 'macchanger -r eth0' and (lines[-1]).rstrip() == 'exit 0':
		second_last_line = (lines[-2] + "macchanger -r eth0\n")
		lines[-2] = second_last_line
	
	# Write the modified list back to the file
	open(file, 'w').writelines(lines)

		
def activate_networkmngr():
	"""Activates the Network-Manager for wired interfaces."""
	print "[*] Activating Network-Manager..."
	for line in fileinput.FileInput("/etc/NetworkManager/NetworkManager.conf",inplace=1):
		print line.replace("managed=false","managed=true").rstrip()
	check_call('service network-manager restart'.split())

	
def main():
	dependencies()
	banner()
	packages()
	desktop_computer_icon()
	set_tweaks()
	mount_smbshare()
	replace_dnssvr()
	random_mac()
	activate_networkmngr()
	

if __name__ == "__main__":
	main()