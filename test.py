#!/usr/bin/python

import subprocess
import os
import wget
import stat



print "downloading with wget"

def check_dependencies():
	 ## check for stuff that is needed to install docker-machine
	 ## dependencies: curl, virtualbox
	return


def install_docker_machine():
	##check_dependencies()

	operating_system_name = os.uname()[0]
	machine_hardware_name = os.uname()[4]
	url = 'https://github.com/docker/machine/releases/download/v0.6.0/docker-machine-'+ os.uname()[0] + '-'+ os.uname()[4]
	new_file_path = "/usr/local/bin/docker-machine"

	file_name = wget.download(url)
	tmp_file_path = os.getcwd() +'/' +file_name 

	os.rename(tmp_file_path, new_file_path)


	st = os.stat(new_file_path)
	os.chmod(new_file_path, st.st_mode | st.st_mode | 0111)

	return



def create_docker_machine_VM():
	# do a check for docker_machine
	os.system('docker-machine create --driver virtualbox default')

	## add eval "$(docker-machine env default)" to bash_profile
	print('Appending docker variables to bash_profile')
	home_dir = os.path.expanduser('~')
	bash_profile_path = home_dir + '/.bash_profile'

	with open(bash_profile_path, "a") as myfile:
		myfile.write("$(docker-machine env default)")

    ## then source bash_profile, so the lastest revisions are applied
	os.system('source .bash_profile')


	return


def install_docker():
	install_docker_machine()
	create_docker_machine_VM()
	return


install_docker()
