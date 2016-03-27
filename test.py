#!/usr/bin/python

import subprocess
import os
import wget
import stat





def install_docker():
	print 'This script will is meant to install docker on OSX'
	print 'It will take care of most of the dependencies'
	print 'Do not be  after to create a bug ticket in github'

	install_docker_machine()
	create_docker_machine_VM()
	return



def install_docker_machine():
	if check_dependencies() :
		operating_system_name = os.uname()[0]
		machine_hardware_name = os.uname()[4]
		url = 'https://github.com/docker/machine/releases/download/v0.6.0/docker-machine-'+ os.uname()[0] + '-'+ os.uname()[4]
		new_file_path = "/usr/local/bin/docker-machine"

		file_name = wget.download(url)
		tmp_file_path = os.getcwd() +'/' +file_name 

		os.rename(tmp_file_path, new_file_path)
		st = os.stat(new_file_path)
		os.chmod(new_file_path, st.st_mode | st.st_mode | 0111)
	else:
		print 'Missing dependencies: virtualbox'

	return




def check_dependencies():
	 ## check for stuff that is needed to install docker-machine
	 ## dependencies: virtualbox
	print 'Checking for dependencies'

	if not check_for_command('virtualbox'):
		install_virtualbox()

	return True




def check_for_command(command):
	
	try :
		command_output  = subprocess.check_output(['which',command])
	except subprocess.CalledProcessError as exc:
		return False
	else: 
		return  not isEmptyString(command_output)


def isEmptyString(str):
        str = str.strip()
        if not str:
                return True
        else:
                return False


def install_virtualbox():

	input = raw_input('Your system is missing virtualbox, Would like us to install it? (Y/N)	')

	if input == 'y' or 'Y':
		url = 'http://download.virtualbox.org/virtualbox/5.0.16/VirtualBox-5.0.16-105871-OSX.dmg'
		file_name = wget.download(url)
		os.system('hdiutil attach '+file_name)
		os.system('installer -package /Volumes/VirtualBox/VirtualBox.pkg -target /')
		os.system('hdiutil detach /Volumes/VirtualBox')
		return True

	if input == 'n' or 'N':
		print(' Script will stop here. Please install virtualbox')
		return False
	
	else: 
		print('Wrong input')
		return False

	return



def create_docker_machine_VM():

	if check_for_command('docker-machine'):

		os.system('docker-machine create --driver virtualbox default')
		## add eval "$(docker-machine env default)" to bash_profile
		print('Appending docker variables to bash_profile')
		home_dir = os.path.expanduser('~')
		bash_profile_path = home_dir + '/.bash_profile'

		with open(bash_profile_path, "a") as myfile:
			myfile.write("eval \"$(docker-machine env default)\"")
	    ## then source bash_profile, so the lastest revisions are applied
		os.system('source ~/.bash_profile')
	else: 
		print 'Missing dependencies: docker_machine'

	return

# Call main function
#install_docker()

create_docker_machine_VM()
