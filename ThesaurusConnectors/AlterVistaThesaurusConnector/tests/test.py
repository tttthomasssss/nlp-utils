import sys
import traceback

from testconfig import config
import requests

from pyvistaconnector import pyvistaconnector

def test_thesaurus_entry_pos_tag_wordnet(api_key=config.get('api_key', None)):

	print '**** [START]: test_thesaurus_entry_pos_tag_wordnet ****'

	# a=ADJ, s=ADJ_SAT, r=ADV, n=NOUN, v=VERB
	wn_pos_tags = ['a', 's', 'r', 'n', 'v']
	words = ['green', 'jealous', 'well', 'love', 'treat']
	d = dict(zip(wn_pos_tags, words))
	for t in wn_pos_tags:
		print 'Running test with PoS Tag=[{}] and word=[{}]...'.format(t, d[t])
		thesaurus_entry_pos_tag_wordnet(t, d[t], api_key)
		print 'Subtest passed!'
		print '-------------------------------------------'

	print '**** [END] ****'
def test_thesaurus_entry_pos_tag_altervista(api_key=config.get('api_key', None)):
	print '**** [START]: test_thesaurus_entry_pos_tag_altervista ****'
	bh_pos_tags = ['(verb)', '(noun)', '(adj)', '(adv)']
	words = ['treat', 'love', 'nice', 'well']
	d = dict(zip(bh_pos_tags, words))
	for t in bh_pos_tags:
		print 'Running test with PoS Tag=[{}] and word=[{}]...'.format(t, d[t])
		thesaurus_entry_pos_tag_altervista(t, d[t], api_key)
		print 'Subtest passed!'
		print '-------------------------------------------'

	print '**** [END] ****'
def test_thesaurus_entry_ngram(api_key=config.get('api_key', None)):
	print '**** [START]: test_thesaurus_entry_ngram ****'
	words = ['ball', 'driver']
	ngrams = [0, 1, 2, 3]
	for ngram in ngrams:
		for word in words:
			print 'Running test with ngram=[{}] for word=[{}] and PoS Tag=[noun]'.format(ngram, word)
			thesaurus_entry_ngram(ngram, word, 'n', api_key)
			print 'Subtest passed!'
			print '-------------------------------------------'
	print '**** [END] ****'

def test_thesaurus_entry_language(api_key=config.get('api_key', None)):
	print '**** [START]: test_thesaurus_entry_language ****'
	words = ['driver', 'love']
	langs = ['en_US', 'de_DE', 'it_IT', 'fr_FR', 'es_ES']
	for word in words:
		for lang in langs:
			print 'Running test with language=[{}] for word=[{}] and PoS Tag=[noun]'.format(lang, word)
			thesaurus_entry_language(lang, word, 'n', api_key)
			print 'Subtest passed!'
			print '-------------------------------------------'
	print '**** [END] ****'

def test_thesaurus_entry_raw_response_format(api_key=config.get('api_key', None)):
	print '**** [START]: test_thesaurus_entry_raw_response_format ****'
	response_formats = [None, 'flam_cheltuk', 'json', 'xml']
	for f in response_formats:
		print 'Running test with word=[love] for response_format=[{}]...'.format(f)
		thesaurus_entry_raw_response_format(f, 'love', api_key)
		print 'Subtest passed!'
		print '-------------------------------------------'
	print '**** [END] ****'

def test_thesaurus_entry_raw_full_response_obj(api_key=config.get('api_key', None)):
	print '**** [START]: test_thesaurus_entry_raw_full_response_obj ****'
	flags = [True, False]
	for f in flags:
		print 'Running test with word=[love] for return_complete_response_obj=[{}]'.format(f)
		thesaurus_entry_raw_full_response_obj(f, 'love', api_key)
		print 'Subtest passed!'
		print '-------------------------------------------'
	print '**** [END] ****'

def test_pos_tag():
	print '**** [START]: test_pos_tag ****'
	wn_pos_tags = ['a', 's', 'r', 'n', 'v']
	wn_pos_tags.append('xxx')
	for t in wn_pos_tags:
		print 'Testing WordNet style -> Big Huge Thesaurus style PoS Tag mapping with WordNet PoS Tag=[{}]'.format(t)
		pos_tag(t)
		print 'Subtest passed!'
		print '-------------------------------------------'
	print '**** [END] ****'

# thesaurus_entry tests
def thesaurus_entry_pos_tag_wordnet(wn_pos_tag, word, api_key):
	result = pyvistaconnector.thesaurus_entry(word=word, api_key=api_key, pos_tag=wn_pos_tag, language='en_US')

	assert(type(result) == list)
	assert(len(result) > 0)


def thesaurus_entry_pos_tag_altervista(bh_pos_tag, word, api_key):
	result = pyvistaconnector.thesaurus_entry(word=word, api_key=api_key, pos_tag=bh_pos_tag, language='en_US')

	assert(type(result) == list)
	assert(len(result) > 0)

def thesaurus_entry_ngram(ngram, word, pos_tag, api_key):
	result = pyvistaconnector.thesaurus_entry(word=word, api_key=api_key, pos_tag=pos_tag, ngram=ngram, language='en_US')

	assert(type(result) == list)

	if (ngram == 0): # Check for words with variable length
		count = result[0].count(' ')
		for res in result[1:]:
			if (count != res.count(' ')):
				break;
		else: # Can assume that test failed
			raise AssertionError
	else:
		for res in result:
			if (res.count(' ') != ngram - 1):
				raise AssertionError

def thesaurus_entry_language(rel_type, word, pos_tag, api_key):
	result = pyvistaconnector.thesaurus_entry(word=word, api_key=api_key, pos_tag=pos_tag, language=rel_type)

	assert(type(result) == list)

# thesaurus_entry_raw tests
def thesaurus_entry_raw_response_format(format, word, api_key):
	result = pyvistaconnector.thesaurus_entry_raw(word=word, api_key=api_key, response_format=format)

	if (format in ['json', 'flam_cheltuk', None]):
		assert(type(result) == dict)
	else:
		assert(type(result) == str)

def thesaurus_entry_raw_full_response_obj(flag, word, api_key):
	result = pyvistaconnector.thesaurus_entry_raw(word=word, api_key=api_key, return_complete_response_obj=flag)

	if (flag):
		assert(type(result) == requests.models.Response)
	else:
		assert(type(result) == dict)

# _big_huge_pos_tag_for_wordnet_pos_tag tests
def pos_tag(wn_pos_tag):
	if (wn_pos_tag == 'a'):
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(adj)')
	elif (wn_pos_tag == 's'):
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(adj)')
	elif (wn_pos_tag == 'r'):
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(adv)')
	elif (wn_pos_tag == 'n'):
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(noun)')
	elif (wn_pos_tag == 'v'):
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(verb)')
	else:
		assert(pyvistaconnector._altervista_pos_tag_for_wordnet_pos_tag(wn_pos_tag) == '(noun)')

# run all
def run_all(api_key):

	try:
		test_thesaurus_entry_pos_tag_wordnet(api_key)
		test_thesaurus_entry_pos_tag_altervista(api_key)
		test_thesaurus_entry_ngram(api_key)
		test_thesaurus_entry_language(api_key)
		test_thesaurus_entry_raw_response_format(api_key)
		test_thesaurus_entry_raw_full_response_obj(api_key)
		test_pos_tag()
	except AssertionError:
		_, _, tb = sys.exc_info()
		traceback.print_tb(tb)

		tb_info = traceback.extract_tb(tb)
		filename, line, func, text = tb_info[-1]
		print 'An error occurred on line {} in statement {}.'.format(line, text)
		exit(1)

if (__name__ == '__main__'):
	if (len(sys.argv) < 2):
		api_key = config.get('api_key', None)
	else:
		api_key = sys.argv[1]

	run_all(api_key)
