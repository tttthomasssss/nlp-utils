#PyVistaConnector

*Simple Connector for the [AlterVistaConnector](http://thesaurus.altervista.org)*

##Installation
`pip install pyvistaconnector`

##Example Usage
```
>>> import pyvistaconnector
>>> pyvistaconnector.thesaurus_entry(
		word='ruby', 
		api_key='<YOUR API-KEY>', 
		pos_tag='n', 
		ngram=2
	)
[u'precious stone', u'transparent gem', u'deep red']
```

##Notes
* Works with NLTK WordNet PoS Tags (i.e. 'n' or `nltk.coprpus.wordnet.NOUN`) as well as the Big Huge Thesaurus PoS Tags.
* By default, it uses `json` and returns a list of results.
* `pyvistaconnector.thesaurus_entry_raw(…)` can be used to retrieve the raw entry returned from the API. *NB: While for `json` responses the return type is a Python `dict`, for `xml` responses the return type is a `str`*.
* And no, the `xml` is not altered/parsed/touched in any way, what you receive is the raw `str` as returned by the API.
* If you want to run the tests locally you need to pass your API key, i.e.: `python test.py <YOUR-API-KEY>`.
* If you want to test with `nose`, you should install `nose-testconfig` (`pip install nose-testconfig`) and create a file called `nose_config.yaml`. The contents of the File should simply be `api_key: <Your API Key>`. You can then run the nose tests with `nosetests -s --tc-file nose_config.yaml --tc-format yaml`. 

## Documentation
Currently available from [here](https://pythonhosted.org/pyvistaconnector/pyvistaconnector.html#module-pyvistaconnector.pyvistaconnector)