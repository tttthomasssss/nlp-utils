import sys
import traceback

import pyhugeconnector

# thesaurus_entry tests
def test_thesaurus_entry_pos_tag_wordnet(wn_pos_tag, word, api_key):
	result = pyhugeconnector.thesaurus_entry(word=word, api_key=api_key, pos_tag=wn_pos_tag, relationship_type='syn', response_callback=None, headers=None)

	assert(type(result) == list)
	assert(len(result) > 0)


def test_thesaurus_entry_pos_tag_bighuge(bh_pos_tag):
	print bh_pos_tag

def test_thesaurus_entry_pos_tag_ngram(ngram):
	None

def test_thesaurus_entry_relationship_type(rel_type):
	None

def test_thesaurus_entry_response_callback(callback):
	None

def test_thesaurus_entry_headers(headers):
	None

# thesaurus_entry_raw tests
def test_thesaurus_entry_raw_response_format(format):
	None

def test_thesaurus_entry_raw_response_callback(callback):
	None

def test_thesaurus_entry_raw_api_version(version):
	None

def test_thesaurus_entry_raw_headers(headers):
	None

def test_thesaurus_entry_raw_full_response_obj(flag):
	None

# _big_huge_pos_tag_for_wordnet_pos_tag tests
def test_pos_tag(wn_pos_tag):
	None

# run all
def run_tests(api_key):
	# a=ADJ, s=ADJ_SAT, r=ADV, n=NOUN, v=VERB
	wn_pos_tags = ['a', 's', 'r', 'n', 'v']
	words = ['green', 'jealous', 'lovely', 'love', 'treat']
	d = dict(zip(wn_pos_tags, words))
	for t in wn_pos_tags:
		print 'Running test with PoS Tag=[{}] and word=[{}]...'.format(t, d[t])
		try:
			test_thesaurus_entry_pos_tag_wordnet(t, d[t], api_key)
		except AssertionError:
			_, _, tb = sys.exc_info()
			traceback.print_tb(tb)

			tb_info = traceback.extract_tb(tb)
			filename, line, func, text = tb_info[-1]
			print 'An error occurred on line {} in statement {}.'.format(line, text)
			exit(1)
		print '-------------------------------------------'

	bh_pos_tags = ['verb', 'noun', 'adjective']
	for t in bh_pos_tags:
		test_thesaurus_entry_pos_tag_bighuge(t)

if (__name__ == '__main__'):
	run_tests(sys.argv[1])
