import os
from scratchclient import ScratchSession
from pydictionary import Dictionary
import random

chars = ['',  '',  '',  '',  '',  '',  '',  '',  '',  'a',  'b',  'c',  'd',  'e',  'f',  'g',  'h',  'i',  'j',  'k',  'l',  'm',  'n',  'o',  'p',  'q',  'r',  's',  't',  'u',  'v',  'w',  'x',  'y',  'z',  '0',  '1',  '2',  '3',  '4',  '5',  '6',  '7',  '8',  '9',  '+',  '-',  '.',  ' ',  '_',  '{', '}',  '"',  ':', "'", '<', '>', ';', ',', '&', '°', '(', ')','?','!']

#encoding (by @wvj)
def encode (val):
    val = val.lower()
    letternum = 1
    val = str(val)
    encoded = ""
    
    for i in range (1,len(str(val))+1):
       encoded = str(encoded) + str(chars.index(val[letternum-1])+1)
       letternum += 1

    return int(encoded + "00")
	
#decoding (by @wvj)
def decode (val):
    letternum = 1
    value = ""
    idx = None
 
    while True:
        val = str(val)
        idx = val[letternum-1] + val[letternum]
        letternum += 2
        if int(idx) < 1:
            break
        value = value + chars[int(idx) - 1]
    return value

#start session
pwd = os.environ['password']
session = ScratchSession("yippymishyTest",  pwd)
connection = session.create_cloud_connection(665490990)

#start listening
oldVal = None

while True:
	cloud = connection.get_cloud_variable("cloud1")
	if not cloud == oldVal:
		if '&' in decode (cloud):
			print ('Message received from user.')
			dict = Dictionary(decode(cloud)[1:len(decode(cloud))])
			meanings_list = dict.meanings()
			#reset the cloud variables
			for i in range (1,5):
					connection.set_cloud_variable('cloud'+str(i),encode(' '))
			#if there is a definition
			if len(meanings_list) > 0:
				print('Returned definition.')
				definition = meanings_list[0]
				print (definition)
				#splitter from pythonexamples.org
				n = 125
				chunks = [definition[i:i+n] for i in range(0, len(definition), n)]
				x = 1
				for i in (chunks):
					connection.set_cloud_variable('cloud'+str(x), encode(i))
					x+=1
			else:
				print ('No definition found.')
				connection.set_cloud_variable('cloud1', encode('No definition found'))

			#tell the Scratch project there is a new message
			connection.set_cloud_variable('catch',random.randint(0,999))
oldVal = cloud