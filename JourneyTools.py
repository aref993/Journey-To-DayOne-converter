# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from time import strftime
from datetime import datetime
import json
import os,glob
import os
from yattag import Doc, indent
import shutil
import xmltodict
from sys import stdout
def getuuid():
	uu=str(uuid.uuid4())
	return uu.replace("-","").upper()
def read_specific_files(pathtodir,filetype):
	all_jrnls_in_array=[]
	os.chdir(pathtodir)
	for anyfile in glob.glob("*."+filetype):
		tmpfile=open(anyfile)
		all_jrnls_in_array.append(tmpfile.read())
	return all_jrnls_in_array
def convert_unixtime(unixtime):
	return datetime.fromtimestamp(int(unixtime)/1000).strftime('%Y-%m-%dT%H:%M:%SZ')

def check_dirs(path):
	os.chdir(path)
	if not os.path.exists('./journal.dayone/'):
		os.makedirs('journal.dayone')
	if not os.path.exists('./journal.dayone/entries/'):
		os.makedirs('./journal.dayone/entries/')
	if not os.path.exists('./journal.dayone/photos/'):
		os.makedirs('./journal.dayone/photos/')
	print 'directory creation done.'
def deserialize_json(allentries):
	loaded=json.loads(allentries)
	return loaded
def convert_to_xml(entry):
	new_uuid=getuuid()
	alluuids.append(new_uuid)
	new_date=convert_unixtime(entry["date_journal"])
	doc, tag, text = Doc().tagtext()
	with tag('plist',Version="1.0"):
		with tag('dict'):
			with tag('key'):
				text('UUID')
			with tag('string'):
				text(new_uuid)
			with tag('key'):
				text('Creation Date')
			with tag('date'):
				text(new_date)
			with tag('key'):
				text('Modified Date')
			with tag('integer'):
				text(str(entry["date_modified"]/1000))
			with tag('key'):
				text('Creator')
			with tag('dict'):
				with tag('key'):
					text('Device Agent')
				with tag('string'):
					text('JourneyTools')
				with tag('key'):
					text('Generation Date')
				with tag('date'):
					text(new_date)
				with tag('key'):
					text('Host Name')
				with tag('string'):
					text('JourneyTools')
				with tag('key'):
						text('OS Agent')
				with tag('string'):
					text('ubuntu')
				with tag('key'):
					text('Software Agent')
				with tag('string'):
					text('JourneyTools')
			with tag('key'):
				text('Entry Text')
			with tag('string'):
				text(entry["text"])
			with tag('key'):
				text('Location')
			with tag('dict'):
				with tag('key'):
					text('Administrative Area')
				with tag('string'):
					text('')
				with tag('key'):
					text('Country')
				with tag('string'):
					text('')
				with tag('key'):
					text('Latitude')
				with tag('real'):
					text(entry["lat"])
				with tag('key'):
					text('Locality')
				with tag('string'):
					text('')
				with tag('key'):
					text('Longitude')
				with tag('real'):
					text(entry["lon"])
				with tag('key'):
					text('Place Name')
				with tag('string'):
					text(entry['address'])
			with tag('key'):
				text('Starred')
			with tag('false'):
				text('')
			with tag('key'):
				text('Time Zone')
			with tag('string'):
				text('Iran Standard Time')
			with tag('key'):
				text('Tags')
			with tag('array'):
				if len(entry['tags'])>0:
					taglist=entry['tags']
					for anytag in taglist:
						with tag('string'):
							text(anytag)
				else:
					text(' ')
				
	result = indent(doc.getvalue(),indentation = ' '*4,newline = '\r\n')
	return result
def convert_main():
	real_path = os.path.dirname(os.path.realpath(__file__))
	alljsons=[]
	alljsons=read_specific_files("./journey/","json")
	os.chdir(real_path)
	print 'we found %d entries to export' %(len(alljsons))
	check_dirs(real_path)
	i=0
	for anyjson in alljsons:
		dj=deserialize_json(anyjson)
		xmltmp=""
		xmltmp=(r'<?xml version="1.0" encoding="UTF-8"?>')
		xmltmp+=(r'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">')
		xmltmp+=(convert_to_xml(dj))
		suuid=alluuids[i]
		i=i+1
		os.chdir(real_path+"/journal.dayone/entries/")
		myfile = open(str(suuid)+".doentry","w")
		myfile.write(xmltmp.encode('utf-8'))
		myfile.close()
		if len(dj['photos'])>0:
			source=real_path+"/journey/"+str(dj['photos'][0])
			target=real_path+"/journal.dayone/photos/"+str(suuid)+".jpg"
			shutil.copyfile(source,target)
		stdout.write("\r%d entry imported successfully" % i)
		stdout.flush()

alluuids=[]	
convert_main()