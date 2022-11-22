""" Service to extract text from a file using Tika
`	Author: Bontenakel Lenny - lennyb.0908@gmail.com
	Created: 23 September 2022
"""
import os
import logging
logging.basicConfig(level = os.environ["LOGLEVEL"] if os.environ["LOGLEVEL"] else "WARNING")
from flask import request

import service


""" Extract text and save it in the triplestore
	@filepath: path to the file relative from FILE_DIR
"""
@app.route("/index", methods=['POST'])
def indexFile():
	body = request.get_json()
	uri = body.get('uri')
	result = service.indexFile(uri)
	return {
		"result": result
	}


""" Extract content and save it for all files
"""
@app.route("/index-all", methods=['POST'])
def indexAll():
	try:
		result = service.indexAll()
	except Exception as e:
		logging.error(e)
		return e
	return {
		"result": result
	}


""" receive a delta signal from the delta notifier service and save the extracted text into the triplestore
	The extracted text will be saved as a predicate of the uploaded file.	
"""
@app.route("/delta", methods=['POST'])
def delta():
	try:
		body = request.get_json()
		target_uri = 'share://'
		uri = ''
		for i in body[0]['inserts']:
			if target_uri in i['subject']['value']:
				uri = i['subject']['value']
		if uri == '': 
			raise Exception("No uri for physical files found. Can not extract content without physical file.")
		result = service.indexFile(uri)
	except Exception as e:
		logging.error(e)
		return e
	return {
		"result": result
	}
