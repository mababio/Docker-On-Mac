#!/usr/bin/python

import subprocess
import os
import wget
import stat





def install_docker():
	print 'This script will is meant to install docker on OSX'
	print 'It will take care of most of the dependencies'
	print 'Do not be  after to create a bug ticket in github'

	install_Docker_Full()
	create_docker_machine_VM()
	return



def install_Docker_Full():

	if check_dependencies() :
		print 'Your system has virtualbox'
		input = raw_input('Your system is missing  the docker suite, Would like us to install it? (Y/N)	')

		if input == 'y' or 'Y':
			url  = 'https://github.com/docker/toolbox/releases/download/v1.10.3/DockerToolbox-1.10.3.pkg'
			file_name = wget.download(url)
			#os.system('hdiutil attach '+file_name)
			os.system('sudo installer -package ' +file_name + ' -target /')
			#os.system('hdiutil detach /Volumes/DockerToolbox')
			return True

		if input == 'n' or 'N':
			print(' Script will stop here. Please install virtualbox')
			return False
		
		else: 
			print('Wrong input')
			return False

		return

	else : 
		print ' You do not have the min requiremnts to procede'




def check_dependencies():
	 ## check for stuff that is needed to install docker-machine
	 ## dependencies: virtualbox
	print 'Checking for dependencies'

	if not check_for_command('VirtualBox'):
		install_virtualbox()

	return True




def check_for_command(command):
	
	try :
		command_output  = subprocess.check_output(['which',command])
	except subprocess.CalledProcessError as exc:
		print 'can not find' + command
		return False
	else: 
		return  not isEmptyString(command_output)


def isEmptyString(str):
        str = str.strip()
        print 'str: for testing --> ' + str
        return not str


def install_virtualbox():

	input = raw_input('Your system is missing virtualbox, Would like us to install it? (Y/N)	')

	if input == 'y' or 'Y':
		url = 'http://download.virtualbox.org/virtualbox/5.0.16/VirtualBox-5.0.16-105871-OSX.dmg'
		file_name = wget.download(url)
		os.system('sudo hdiutil attach '+file_name)
		os.system('sudo installer -package /Volumes/VirtualBox/VirtualBox.pkg -target /')
		os.system('sudo hdiutil detach /Volumes/VirtualBox')
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
		print 'docker-machine is installed. We can procede'
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
install_docker()
#create_docker_machine_VM()
