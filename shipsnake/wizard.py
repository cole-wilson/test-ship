import os
import glob
import toml
import sys


questions = {
	"name":"Full name of project",
	"short_name":"Short name of project",
	"author":"Your name(s)",
	"email":"Project email",
	"short_description":"Short description of your project",
	"description":"Full description of your project",
	"url":"Main project URL",
	"license":"License",
	"keywords":"Keywords seperated with a space",
	"data_files":"Data files (with *) to include in project seperated with a space",
	"file":"Main python file, leave blank for no main file",
	"modules":"Required modules, seperated with space"
}
questions2= {
	"type":"Please choose one of the following options for your project:\n\t1. My project only deals with text (not graphical).\n\t2. My project is a graphical app.\n>>>",
	"mac":"Would you like to distribute a Mac app for your project? [y/n]",
	"windows":"Would you like to distribute a Windows app for your project? [y/n]",
}


def main():
	prefix = os.path.dirname(os.path.abspath(__file__))
	data = {}
	if os.path.isfile('.'+os.sep+'shipsnake.toml'):
		data = toml.loads(open('.'+os.sep+'shipsnake.toml').read())
	print("I'm going to ask you a few questions about your project to create a config file!\n\nPlease fill in everything to your ability. If you can't provide a value, leave it blank.\n")

	for key in questions:
		if key not in data:
			if len(glob.glob('.'+os.sep+'LICENS*'))>0 and key=="license":
				print('\033[1;34mYou seem to have a license file in your project, but what type is it?')
				for license in "AGPL-3.0/Apache-2.0/BSD-2-Clause/BSD-3-Clause/GPL-2.0/GPL-3.0/LGPL-2.1/LGPL-3.0/MIT".split(os.sep+''):
					print(f'\t- {license}')
				data[key] = input(">>>\033[0m ")
			elif len(glob.glob('.'+os.sep+'LICENSE*'))==0 and key=="license":
				data[key]=""
			elif key=="data_files" or key=="modules":
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ").split(' ')
			else:
				data[key] = input("\033[1;34m"+questions[key]+":\033[0m ")
		else:
			print("\033[1;34m"+str(questions[key])+":\033[0m "+str(data[key]))
	if "build" not in data:
		data['build']={}
	for key in questions2:
		if key not in data['build']:
			data['build'][key] = input("\033[1;34m"+questions2[key]+"\033[0m ")
		else:
			print("\033[1;34m"+str(questions2[key])+"\033[0m "+str(data['build'][key]))
	if (data['build']['mac'][0]=="y" or data['build']['windows'][0]=="y"):
		if 'installer' in data['build']:
			print("\033[0m"+"Would you like to provide an installer for the app(s)? (reccomended) [y/n]"+"\033[0m "+data['build']['installer'])
		else:
			data['build']['installer'] = input("\033[1;34m"+"Would you like to provide an installer for the app(s)? (reccomended) [y/n]"+"\033[0m ")

	if not sys.platform.startswith('win') and data['build']['windows']=='y':
		print('\033[1;31mYou can only make a Windows app on a Windows computer.\033[0m')
		needswin=True
	if sys.platform != 'darwin' and data['build']['mac']=='y':
		print('\033[1;31mYou can only make a Mac app on a Mac.\033[0m')
		needsmac=True
	if needsmac or needswin:
		actions = input('\033[1;34mGithub Actions can build your app on the cloud for free.\n\033[0mWould you like to use that to build your apps? [y/n] \033[0m')
		data['build']['ations'] = actions
	if actions[0]=='y':

		print('\033[1;31mI have created the neccesary files in your project. Please upload this folder to GitHub to use this feature.\n\n\033[0mFor help, see https://docs.github.com/en/free-pro-team@latest/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line\033[0m')
	# if not os.path.isfile('.'+os.sep+'README.md'):
	open('README.md','w+').write(open(prefix+os.sep+'readme.template').read().format(**data))
	
	f = open('.'+os.sep+'shipsnake.toml','w+')
	f.write(toml.dumps(data))
	f.close()