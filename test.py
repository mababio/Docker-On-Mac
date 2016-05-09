#!/usr/bin/env

import subprocess
import os
import wget
import stat
import urllib2

docker_suite_url  = 'https://github.com/docker/toolbox/releases/latest'
#'https://github.com/docker/toolbox/releases/download/v1.10.3/DockerToolbox-1.10.3.pkg'
#https://github.com/docker/toolbox/releases/download/v1.11.1b/DockerToolbox-v1.11.1b.pkg



def install_docker():
	print 'This script will is meant to install docker on OSX'
	print 'It will take care of most of the dependencies'
	print 'Do not be  after to create a bug ticket in github'

	install_Docker_Full()

	#if test_docker_install():
		#create_docker_machine_VM()
	#else:
	#	print 'Failed test phase!'

	return



def install_Docker_Full():

	print 'About to download Docker toolbox'

	input = raw_input('Your system is missing  the docker suite, Would like us to install it? (Y/N)	')

	if input == 'y' or 'Y':
		try:
			url = get_latest_docker_link(docker_suite_url)
			file_name = wget.download(url)
			os.system('sudo installer -package ' +file_name + ' -target /')
		except:
			print 'Failed to download Docker toolbox'
		return True

	elif input == 'n' or 'N':
		print(' Script will stop here. Please install virtualbox')
		return False
	
	else: 
		print('Wrong input')
		return False

def get_latest_docker_link(link):
		req = urllib2.Request(docker_suite_url)
		res = urllib2.urlopen(req)
		verison = res.geturl().split('/')[-1][1:-1]
		return 'https://github.com/docker/toolbox/releases/download/v'+verison+'/DockerToolbox-'+verison+'.pkg'
				


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
