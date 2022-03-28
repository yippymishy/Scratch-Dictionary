import os
import scratchconnect
from pydictionary import Dictionary
import random

chars = ['','',  '',  '',  '',  '',  '',  '',  '',  '',  'a',  'b',  'c',  'd',  'e',  'f',  'g',  'h',  'i',  'j',  'k',  'l',  'm',  'n',  'o',  'p',  'q',  'r',  's',  't',  'u',  'v',  'w',  'x',  'y',  'z',  '0',  '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9',  '+',  '-',  '.',  ' ',  '_',  '{', '}',  '"',  ':', "'", '<', '>', ';', ',', '&', '°', '(', ')','?','!','×']

#encoding (by @wvj)
def encode (text):
	i = 0
	encoded = ''
	text = text.lower()
	
	for loop in range (0,len(text)):
		encoded = encoded + str(chars.index (text[i]))
		i+=1
		
	return (int(encoded+'00'))
	
#decoding (by @wvj)
def decode (text):
	i = 0
	decoded = ''
	text = str(text)

	for loop in range (int(len(text)/2)):
		decoded = f'{decoded}{chars [int(text[i]+text[i+1])]}'
		i += 2

	return (decoded)

#start session
password = os.environ['pwd']
user = scratchconnect.ScratchConnect("yippymishyTest", password)

#user = scratchconnect.ScratchConnect("yippymishyTest", pwd)
project = user.connect_project(project_id=665490990)
variables = project.connect_cloud_variables()

#start listening
oldVal = None

while True:
	cloud = variables.get_cloud_variable_value(variable_name="cloud1")[0]
	decoded = decode(cloud)
	if not cloud == oldVal:
		if '&' in decoded:
			dict = Dictionary(decode(cloud)[1:len(decode(cloud))])
			meanings_list = dict.meanings()
			#reset the cloud variables
			for i in range (1,5):
					set = variables.set_cloud_variable (variable_name="cloud"+str(i), value=encode(''))
			#if there is a definition
			if len(meanings_list) > 0:
				definition = meanings_list[0]
				#splitter from pythonexamples.org
				n = 125
				chunks = [definition[i:i+n] for i in range(0, len(definition), n)]
				x = 1
				for i in (chunks):
					set = variables.set_cloud_variable (variable_name="cloud"+str(x), value=encode(i))
					x+=1
			else:
				set = variables.set_cloud_variable (variable_name="cloud1", value=encode('Failed; you most likely spelled the word wrong.'))

			#tell the Scratch project there is a new message
			set = variables.set_cloud_variable(variable_name="catch", value=random.randint(0,999))
oldVal = cloud
