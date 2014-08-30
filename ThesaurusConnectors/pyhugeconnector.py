import sys

import requests

def _big_huge_pos_tag_for_wordnet_pos_tag(pos_tag):
	"""Convert the given WordNet style PoS Tag into a Big Huge Thesaurus Style PoS Tag

		Keyword arguments:
		pos_tag -- The WordNet style PoS Tag (mandatory, no default)
	"""
	tag = 'noun'

	if (pos_tag == 'v'):
		tag = 'verb'
	elif (pos_tag == 'a' or pos_tag == 'r'): # a=adjective, r=adverb
		tag = 'adjective'

	return tag

def thesaurus_entry_raw(word, api_key, response_format='json', response_callback=None, api_version='2', headers=None, return_complete_response_obj=False):
	"""Return the raw Thesaurus entry for the given word (in the given response format)

		Keyword arguments:
		word -- The word to look up (mandatory, no default)
		api_key -- Your API Key for the Big Huge Thesaurus, get your key here: https://words.bighugelabs.com/getkey.php (mandatory, no default)
		response_format -- Desired format of the response, possible options are 'json', 'xml' and 'php', see https://words.bighugelabs.com/api.php for more details (default 'json')
		response_callback -- Callback function to be invoked after request (default None)
		api_version -- Version of the Big Huge Thesaurus API (override at your own risk!) (default '2')
		headers -- Custom headers to be used for the request (default None)
		return_complete_response_obj -- Returns the full python-requests (http://docs.python-requests.org/en/latest/) response object (default False)
	"""

	# Specify response format
	if (response_format != None):

		# Quick Sanity Check
		if (not response_format.lower() in ['xml', 'json', 'php']):
			response_format = 'json'
	else:
		response_format = 'json'

	# Create Request URL
	url = 'http://words.bighugelabs.com/api/{}/{}/{}/{}'.format(api_version, api_key, word, response_format)

	r = requests.get(url, params={'callback': response_callback}, headers=headers) if response_callback else requests.get(url, headers=headers)

	# Raise if the request failed
	r.raise_for_status()

	# If format is not json, then the content is returned, to be parsed by the client
	return r if return_complete_response_obj else (r.json() if response_format == 'json' else r.content)

def thesaurus_entry(word, api_key, pos_tag='n', ngram=0, relationship_type=None, response_callback=None, headers=None):
	"""Return the Thesaurus entry for the given word.

		Keyword arguments:
		word -- The word to look up (mandatory, no default)
		api_key -- Your API Key for the Big Huge Thesaurus, get your key here: https://words.bighugelabs.com/getkey.php (mandatory, no default)
		pos_tag -- WordNet style (i.e. 'n', 'v', nltk.corpus.wordnet.NOUN) or Big Huge Thesaurus style PoS Tag (i.e. 'noun', 'verb') (default 'n')
		ngram -- Filter for specific n-grams, pass ngram=0 to get all n-grams (default 0)
		relationship_type -- Use 'syn' for synonyms, 'ant' for antonyms, 'rel' for related terms, 'sim' for similar terms, 'usr' for user suggestions and None for all (default None)
		response_callback -- Callback function to be invoked after request (default None)
		headers -- Custom headers to be used for the request (default None)
	"""

	# Map WordNet PoSTag to BigHuge PoSTag (if it is a WordNet PoS Tag)
	pos_tag = _big_huge_pos_tag_for_wordnet_pos_tag(pos_tag) if len(pos_tag) == 1 else pos_tag

	# Result is a dict of dicts
	result = thesaurus_entry_raw(word=word, api_key=api_key, response_format='json', response_callback=response_callback, headers=headers)
	result_by_pos_tag = result.get(pos_tag, None)

	# Fiddle out the given relationship_type entry
	if (result_by_pos_tag != None and relationship_type != None):

		# Filter by ngram
		if (ngram > 0):
			return [rel_type for rel_type in result_by_pos_tag.get(relationship_type, None) if rel_type.count(' ') == (ngram - 1)]
		else:
			return [rel_type for rel_type in result_by_pos_tag.get(relationship_type, None)]

	return result_by_pos_tag

if (__name__ == '__main__'):
	if (len(sys.argv) >= 3):
		word = sys.argv[1]
		api_key = sys.argv[2]
		pos_tag = sys.argv[3] if len(sys.argv) > 3 else 'n'
		ngram = int(sys.argv[4]) if len(sys.argv) > 4 else 1
		rel_type = sys.argv[5] if len(sys.argv) > 5 else 'syn'
		response_callback = sys.argv[6] if len(sys.argv) > 6 else None
		headers = sys.argv[7] if len(sys.argv) > 7 else None

		print thesaurus_entry(word=word, api_key=api_key, pos_tag=pos_tag, ngram=ngram, relationship_type=rel_type, response_callback=response_callback, headers=headers)
	else:
		print 'Not enough args, need to specify at least \'word\' and \'api_key\'; i.e.: python pyhugeconnector.py love XXXAPIKEY666'
