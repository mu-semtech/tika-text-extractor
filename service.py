""" Service to extract text from a file using Tika
`	Author: Bontenakel Lenny - lennyb.0908@gmail.com
	Created: 23 September 2022
"""
import os
import logging
logging.basicConfig(level = os.environ["LOGLEVEL"])

import tika #https://github.com/chrismattmann/tika
tika.initVM()
from tika import parser

from string import Template
from helpers import query
from escape_helpers import *


""" index physical file
	@params:
	- uri: uri of a physical file
"""
def indexFile(uri):
	path = uri.replace('share://', '/share/')
	try:
		fileContent = parser.from_file(path)["content"]
	except FileNotFoundError as e:
		logging.error(e)
		return e
	virtualFileURI = queryDataSource(uri)
	if virtualFileURI == "":
		logging.info(f"No Datasource found for {uri}. Skipping.")
		return
	result = saveContent(virtualFileURI, fileContent)
	return result


""" Index saved physical files 
"""                                                
def indexAll():
	uris = queryFileURIs()
	physicalURIs = [ i for i in uris if 'share://' in i ]
	for i in physicalURIs:
		logging.info(f"INDEXING {i}")
		indexFile(i)
	return "success"


""" save text from a file into a triple store
	@params:
	- uri: uri of the virtual file to save the text on
	- content: extracted text to save 
"""
def saveContent(uri, content, graph=os.environ.get("DEFAULT_GRAPH")):	
	query_string = Template("""
		PREFIX sioc: <http://rdfs.org/sioc/ns#>	

		DELETE {
			GRAPH $graph {
				$uri sioc:content ?o . 	
			}		
		}
		INSERT { 
			GRAPH $graph {
				$uri sioc:content $content . 
			} 
		}"""
	).substitute(
		uri=sparql_escape_uri(uri),
		content=sparql_escape_string(content),
		graph=sparql_escape_uri(graph),
	)
	query_result = query(query_string)
	return query_result


""" get the uuids of all physical files	
	@returns: list of uuids
"""
def queryFileURIs():
	query_string = """
		prefix nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#> 

		select distinct(?uri) {
			?uri a nfo:FileDataObject .
		}"""	
	query_result = query(query_string)['results']['bindings']
	fileUuids = [ i['uri']['value'] for i in query_result ]
	return fileUuids


""" Find the physical path of a file based on its uuid
	@params:
	- uri: uri of a file
	@returns:
	- fileName: name of the file
"""
def queryFileName(uri):
	query_string = Template("""
		prefix nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#> 

		select ?fileName {
			$uri nfo:fileName ?fileName .
		}"""	
	).substitute(
		uri=sparql_escape_uri(uri)
	)
	query_result = query(query_string)['results']['bindings']
	if(len(query_result) <= 0): 
		return ""
	fileName = query_result[0]['fileName']['value']
	return fileName


""" Get the data source of a physical file
	@params:
	- uri: uri of a physical file
	@returns:
	- dataSource: IRI of corresponding virtual file
"""
def queryDataSource(uri):
	query_string = Template("""
		prefix nie: <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#> 

		select ?dataSource {
			$uri nie:dataSource ?dataSource .
		}"""
	).substitute(
		uri=sparql_escape_uri(uri)
	)
	query_result = query(query_string)['results']['bindings']
	if(len(query_result) <= 0): 
		return ""
	dataSource = query_result[0]['dataSource']['value']
	return dataSource	


""" check if a file is already indexed
	@params:
	- uri: uri of a virtual file
	@returns:
	- content: content of a file
"""
def queryContent(uri):
	query_string = Template("""
		PREFIX sioc: <http://rdfs.org/sioc/ns#>	

		select ?content {
			$uri sioc:content ?content .
		}"""
	).substitute(
		uri=sparql_escape_uri(uri)
	)
	query_result = query(query_string)['results']['bindings']
	if(len(query_result) <= 0): 
		return ""
	content = query_result[0]['content']['value']
	return content	


