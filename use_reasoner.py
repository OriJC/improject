import os
import re
import subprocess
import platform

URI = 'http://attempto.ifi.uzh.ch/ontologies/owlswrl/test'
reasoner = 'HermiT.jar'
ape = 'ape'
owl_to_ace = 'owl_to_ace'
demo_class = 'Demo'

debug = True

# Get the commands formating right for the right operating system
plat = platform.system()
exe_head, exe_tail = '', '.exe'
if plat != "Windows":
	exe_head = './'

ape_command = lambda filename: [f'{exe_head}{ape}{exe_tail}', '-file', filename, '-solo', 'owlxml', '-guess']
owl_to_ace_command = lambda filename: [f'{exe_head}{owl_to_ace}{exe_tail}', '-xml', filename]

if not os.path.exists(reasoner):
	print("Cannot find reasoner.")

if not os.path.exists(f'{ape}{exe_tail}'):
	print("Cannot find ape")

if not os.path.exists(f'{owl_to_ace}{exe_tail}'):
	print("Cannot find owl_to_ace")

# compiling Demo.class
if not os.path.exists(f'{demo_class}.class'):
	subprocess.run(
		['javac',
		 '-cp',
		 reasoner,
		 f'{demo_class}.java'])

def ace_to_owl(string: str, directory: str) -> str:
	"""Write the ACE string into a OWL file (XML format)

	- This is a function acting as a proof of concept rather than actually being used

	Args:
		string (str): the ACE string that needs to be translated
		directory (str): the directory in which the file is saved as (*.owl)
	"""
	string.replace('\n', ' ')
	with open(f'./capture/{directory}.owl', 'w') as file:
		s = subprocess.run([f'{exe_head}{ape}{exe_tail}', 
							'-text', f'{string}', 
							'-solo', 'owlxml', 
							'-guess'],
						   capture_output=True)
		file.write(str(s.stdout.decode('utf-8')))
	file.close()

def run_deprecated(storypath, querypath):
	with open(f'{storypath}.owl', 'wb') as file:
		s = subprocess.run(ape_command(filename = storypath), capture_output = True)
		file.write(s.stdout)
	with open(f'{querypath}.owl', 'wb') as file:
		q = subprocess.run(ape_command(filename = querypath), capture_output = True)
		file.write(re.sub(b'ontologyIRI=".*"', b'ontologyIRI=""', q.stdout))
	result = subprocess.run(
		['java',
		 '-cp',
		 f'''.{';' if plat == 'Windows' else ':'}{reasoner}''',
		 demo_class,
		 'e',
		 os.path.abspath(f'{storypath}.owl'),
		 os.path.abspath(f'{querypath}.owl')], capture_output = True, shell = (True if plat == 'Windows' else False))
	#print(result.stdout)
	if not debug:
		os.remove(f'{storypath}.owl')
		os.remove(f'{querypath}.owl')
	if b'true' in result.stdout:
		return 'True'
	elif b'false' in result.stdout:
		return 'False'
	else:
		return result.stdout.decode()

def run(storypath: str, querypath: str):
	# java -cp seperator
	if plat == 'Windows': 
		seperator = ';'
	else:
		seperator = ':'
	
	result = subprocess.run(
		['java',
		 '-cp',
		 f'.{seperator}{reasoner}',
		 demo_class,
		 'e',
		 os.path.abspath(f'./capture/{storypath}.owl'),
		 os.path.abspath(f'./capture/{querypath}.owl')],
		 capture_output = True, 
		 shell = True)
	
	print("This", result.stdout)
	
	if not debug:
		os.remove(f'{storypath}.owl')
		os.remove(f'{querypath}.owl')

	if b'true' in result.stdout:
		return 'True'
	elif b'false' in result.stdout:
		return 'False'
	else:
		return result.stdout.decode('utf-8')
