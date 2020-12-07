if __name__ != '__main__':
	print("Please run shipsnake as script or command, not module.")
import toml
import os
import sys
import glob
import shutil

# mode = sys.argv[1]
# mode="upload"
version = ""
if len(sys.argv) == 1:
	print("Provide a mode:\n\tshipsnake [wizard | build | dev | upload]")
	sys.exit(0)
mode = sys.argv[1]
if len(sys.argv) < 3 and mode in ["upload",'build']:
	print("Provide a version:\n\tshipsnake "+mode+" <version>")
	sys.exit(0)
if len(sys.argv)>2:
	version = sys.argv[2]
if mode=="dev" and version=="":
	version = "dev_build"



if os.getenv('TEST_SNAKE')=="TRUE":
	os.chdir('tester')


if mode == "wizard":
	import wizard
	wizard.main()

elif mode in ["build","dev","upload"]:
	open('.'+os.sep+'.gitignore','w+').write('*'+os.sep+'__pychache__')
	if not os.path.isfile('.'+os.sep+'shipsnake.toml'):
		print('Please create a config file with `shipsnake wizard` first.')
		sys.exit(0)
	with open('.'+os.sep+'shipsnake.toml') as datafile:
		data = toml.loads(datafile.read())
	with open(prefix+os.sep+'setup.py.template') as datafile:
		template = datafile.read()
	setup = template.format(
		**data,
		version = version,
		entry_points = [data["short_name"]+"="+data["short_name"]+".__main__"] if data["file"]!="" else [""]
	)
	open('setup.py','w+').write(setup)
	source_dir = os.getcwd()
	target_dir = data["short_name"]+os.sep
	types = ('*.py',*data["data_files"])
	file_names = []
	for files in types:
		file_names.extend(glob.glob(files))
	if not os.path.isdir(target_dir):
		os.mkdir(target_dir)
	for file_name in file_names:
		if file_name in ["setup.py","shipsnake.toml"]:
			continue
		shutil.move(os.path.join(source_dir, file_name), target_dir+os.sep+file_name)
	open(target_dir+'__init__.py','w+').write('')
	if data['file']!="" and not os.path.isfile(data['short_name']+os.sep+'__main__.py'):
		try:
			os.rename(data['short_name']+os.sep+data['file'],data['short_name']+os.sep+'__main__.py')
			open(data['short_name']+os.sep+data['file'],'w+').write('# Please edit __main__.py for the main code. Thanks!\n(you can delete this file.)')
		except FileNotFoundError:
			pass
	try:
		shutil.rmtree('dist')
	except:
		pass
	try:
		os.mkdir('bin')
	except:
		pass
	open("bin"+os.sep+data['short_name'],'w+').write(f"#!"+os.sep+"usr"+os.sep+"bin"+os.sep+f"env bash\npython3 -m {data['short_name']} $@ || echo 'Error. Please re-install shipsnake with:\\n`pip3 install shipsnake --upgrade`'")
	if mode == "build" or mode=="upload":
		os.system('python3 .'+os.sep+'setup.py sdist bdist_wheel')
		try:
			shutil.rmtree('build')
		except:
			pass
	elif mode == "dev":
		os.system('python3 .'+os.sep+'setup.py develop')
	for x in glob.glob('*.egg-info'):
		shutil.rmtree(x)
else:
	print(f'Illegeal option `{mode}`')
	sys.exit(0)

if mode=="upload":
	print("Please make sure that you have a https://pypi.org/ account.")
	try:
		import twine
	except:
		input('Press enter to continue installing `twine`. Press ctrl+x to exit.')
		os.system('python3 -m pip install --user --upgrade twine || python3 -m pip install --upgrade twine')
	os.system('python3 -m twine upload dist'+os.sep+'*')
