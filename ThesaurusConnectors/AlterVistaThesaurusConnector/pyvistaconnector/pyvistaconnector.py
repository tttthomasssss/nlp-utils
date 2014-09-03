import sys

import requests

def _altervista_pos_tag_for_wordnet_pos_tag(pos_tag):
	tag = '(noun)'

	if (pos_tag == 'v'): # v=verb
		tag = '(verb)'
	elif (pos_tag == 'a' or pos_tag == 's'): #a=adjective, s=satellite adjective
		tag = '(adjective)'
	elif (pos_tag == 'r'): #r=adverb
		tag = '(adverb)'

	return tag

def thesaurus_entry_raw(word, api_key, response_format='json', language='en_US', return_complete_response_obj=False):
	# Specify response format
	if (response_format != None):

		# Quick Sanity Check
		if (not response_format.lower() in ['xml', 'json']):
			response_format = 'json'
	else:
		response_format = 'json'

	url = 'http://thesaurus.altervista.org/thesaurus/v1'

	params = {
		'key':		api_key,
		'word':		word,
		'language':	language,
		'output':	response_format
	}

	r = requests.get(url, params=params)

	# Raise if the request failed
	r.raise_for_status()

	# If format is not json, then the content is returned, to be parsed by the client
	return r if return_complete_response_obj else (r.json() if response_format == 'json' else r.content)

def thesaurus_entry(word, api_key, pos_tag, ngram=0, language='en_US'):
	# Map WordNet PoSTag to BigHuge PoSTag (if it is a WordNet PoS Tag)
	if (pos_tag != None):
		pos_tag = _altervista_pos_tag_for_wordnet_pos_tag(pos_tag) if len(pos_tag) == 1 else pos_tag

	# Result is a dict of lists (of dicts (of dicts)) <-- oh yes, its an *awesome* json response format
	result = thesaurus_entry_raw(word=word, api_key=api_key, response_format='json')
	result_list = result.get('response', [])

	# Unpack the shit
	result_list = map(lambda entry: entry.get('list', {'category': 'fail', 'synonyms':''}), result_list)

	# More unpacking
	result_list = map(lambda entry: entry.get('synonyms', '').split('|') if entry.get('category', '') == pos_tag else [], result_list)

	# Flatten, filter the empty lists and filter for the correct ngram
	result = []
	for entry_list in result_list:
		for entry in entry_list:
			sanitised_entry = entry[:entry.index('(')].strip() if ('(' in entry and ')' in entry) else entry
			if (sanitised_entry.count(' ') == (ngram - 1)):
				result.append(sanitised_entry)

	return result

if (__name__ == '__main__'):
	if (len(sys.argv) >= 4):
		word = sys.argv[1]
		api_key = sys.argv[2]
		pos_tag = sys.argv[3]
		ngram = int(sys.argv[4]) if len(sys.argv) > 4 else 1
		language = sys.argv[5] if len(sys.argv) > 5 else 'en_US'

		print thesaurus_entry(word=word, api_key=api_key, pos_tag=pos_tag, ngram=ngram, language=language)
	else:
		print 'Not enough args, need to specify at least \'word\', \'api_key\' and \'pos_tag\'; i.e.: python pyhugeconnector.py love XXXAPIKEY666 noun'

