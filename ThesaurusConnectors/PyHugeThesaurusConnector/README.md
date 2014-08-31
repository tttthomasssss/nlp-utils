#PyHugeConnector

*Simple Connector for the [BigHugeThesaaurus](https://words.bighugelabs.com)*

##Installation
`pip install pyhugeconnector`

##Example Usage
```
>>> import pyhugeconnector
>>> pyhugeconnector.thesaurus_entry(
		word='love', 
		api_key='<YOUR-API-KEY>', 
		pos_tag='n', 
		ngram=2, 
		relationship_type='syn'
	)
[u'sexual love', u'erotic love', u'making love', u'love life', u'loved one', u'physical attraction', u'sex activity', u'sexual activity', u'sexual desire', u'sexual practice']
```

##Notes
* Works with NLTK WordNet PoS Tags (i.e. 'n' or `wordnet.NOUN`) as well as the Big Huge Thesaurus PoS Tags.
* By default, it uses `json` and returns a list of results
* `pyhugeconnector.thesaurus_entry_raw(…)` can be used to retrieve the raw entry returned from the API. *NB: While for `json` responses the return type is a Python `dict`, for `xml` or `php` responses the return type is a `str`.
* And no, neither `xml` or `php` are altered/parsed/touched in any way, what you receive is the raw `str` as returned by the API.
* If you want to run the tests locally you need to pass your API key, i.e.: `python test.py <YOUR-API-KEY>`
* If you want to test with `nose`, you should install `nose-testconfig` (`pip install nose-testconfig`) and create a file called `nose_config.yml`. The contents of the File should simply be `api_key: <Your API Key>`. You can then run the nose tests with `nosetests -s --tc-file nose_config.yaml --tc-format yaml`  
