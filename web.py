""" Service to extract text from a file using Tika
`	Author: Bontenakel Lenny - lennyb.0908@gmail.com
	Created: 23 Septembre 2022
"""

from urllib import request
from string import Template
from helpers import query
from escape_helpers import sparql_escape_uri

import tika # https://github.com/chrismattmann/tika-python
tika.initVM()
from tika import parser


# TODO delete route this later
@app.route("/hello")
def hello():
    return "Hello from the mu-python-template!"

""" receive a logical file and attach the extracted text from it
	Files are uploaded to this endpoint using the mu-semtech/file-service (https://github.com/mu-semtech/file-service)
	@file: the file from which to extract text
"""
@app.route("/extract", methods=['POST'])
def extractText():
	 
	file = request.args.get("file")
	
	extractedText = parser.from_file(filepath)
	return extractedText
	
	
""" save text from a file into a triple store
 
"""
def saveExtractedText(fileId, extractedText):
	query_template = Template("""
	PREFIX files: <http://lynx.lblod.info/files/>
	PREFIX ext: <http://mu.semte.ch/vocabularies/ext/> 

	INSERT DATA { GRAPH {
		files:$fileId ext:extractedText $extractedText .froggy 
		} 
	}
	""")
	query_string = query_template.substitute(
		fileId=sparql_escape_uri(fileId),
		extractedText=sparql_escape_uri(extractedText)
	)
	
	query_result = query(query_string)
	return query_result
	
	
""" receive a triple and search the database what to extract
	
"""
@app.route("/delta", methods=['POST'])
def receiveTriple():
	return "where is the triple?"
	