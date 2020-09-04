# emCoNLL

emCoNLL is a (half-baked) script converting [emtsv](https://github.com/dlt-rilmta/emtsv) output to **CoNLL-U** format.

What's in this repo:

* [converter.py](emconll/converter.py) the script itself
* [vizilo.tsv](tests/vizilo.tsv) small input example
* [vizilo.conll](tests/vizilo.conll) small output example
* [conll_features](docs/conll_features) about the formats

Usage:
`python3 -m emconll -i vizilo.tsv > vizilo.conll`

There are options to support the standardish variaton of the format:

- `--print-header`: Print header (useful, but not required for CoNLL-U)
- `--force-id`: Generate IDs when no dependency parse present
- `--add-space-after-no`: If misc column is empty and tokenisation information (wsafter column) is present, add `SpaceAfter=no` when needed
- `--extra-columns key1:val1,key2:val2`: Add extra columns after the mandatory 10 columns using the available ones: keys (e.g. key1, key2) are the existing column names which will be converted to the desired names denoted by vals (e.g. val1, val2)
