#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xtsv import build_pipeline, parser_skeleton


def main():

    argparser = parser_skeleton(description='emCoNLL - a script converting emtsv output to CoNLL-U format')
    opts = argparser.parse_args()

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['conll']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    # from emdummy import DummyTagger
    em_conll = ('emconll.converter', 'EmCoNLL', 'CoNLL-U converter', (),
                {'source_fields': {'form'}, 'target_fields': []})
    tools = [(em_conll, ('conll', 'emCoNLL'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets))


if __name__ == '__main__':
    main()
