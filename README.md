# emCoNLL

emCoNLL is a (half-baked) script converting [emtsv](https://github.com/dlt-rilmta/emtsv) output to **CoNLL-U** format.

What's in this repo:

* [converter.py](emconll/converter.py) the script itself
* [vizilo.tsv](tests/vizilo.tsv) small input example
* [vizilo.conll](tests/vizilo.conll) small output example
* [conll_features](docs/conll_features) about the formats

Usage:
`python3 -m emconll -i vizilo.tsv > vizilo.conll`
