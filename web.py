""" Service to extract text from a file using Tika
`	Author: Bontenakel Lenny - lennyb.0908@gmail.com
	Created: 23 September 2022
"""

import os
import logging
from requests import request
logging.basicConfig(level=os.environ.get("LOGLEVEL"))

from flask import request

import tika #https://github.com/chrismattmann/tika-python
tika.initVM()
from tika import parser

from string import Template
from helpers import query
from escape_helpers import sparql_escape_uri


""" receive a logical file and attach the extracted text from it
	Files are uploaded to this endpoint using the mu-semtech/file-service (https://github.com/mu-semtech/file-service)
	@file: the file from which to extract text
"""
@app.route("/extract", methods=['GET'])
def extractText():	
	args = request.args
	file = args.get("file")
	try:
		extractedText = parser.from_file(f"/share/{file}")
		# TODO: save the metadata and content in the triplestore
		return {
			"metadata": extractedText["metadata"],
			"content": extractedText["content"] 
		}
	except Exception as e:		
		return e.__repr__
	
	
""" save text from a file into a triple store
 
"""
def saveExtractedText(fileId, metadata, extractedText):
	query_template = Template("""
		PREFIX files: <http://lynx.lblod.info/files/>
		PREFIX ext: <http://mu.semte.ch/vocabularies/ext/> 

		INSERT DATA { GRAPH <$GRAPH> {
			files:$fileId ext:extractedText $extractedText ; 
				ext:metadata $metadata .
			} 
		}
	""")	
	query_string = query_template.substitute(
		GRAPH="",
		fileId=sparql_escape_uri(fileId),
		extractedText=sparql_escape_uri(extractedText),
		metadata=sparql_escape_uri(metadata)
	)
	query_result = query(query_string)
	return query_result
	
	
""" receive a triple and search the database what to extract
	
"""
@app.route("/delta", methods=['POST'])
def receiveTriple():
	return "where is the triple?"
	