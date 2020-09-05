#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xtsv import build_pipeline, parser_skeleton, add_bool_arg


def main():

    argparser = parser_skeleton(description='emCoNLL - a script converting emtsv output to CoNLL-U format')
    add_bool_arg(argparser, 'print-header', 'Print header')
    add_bool_arg(argparser, 'force-id', 'Force writing ID field when it is not available')
    add_bool_arg(argparser, 'add-space-after-no', 'Add SpaceAfter=no to misc when wsafter field present')
    argparser.add_argument('--extra-columns', dest='extra_columns',  type=str, default=None,
                           help='Add extra columns in key1:val1,key2:val2 format')
    opts = argparser.parse_args()
    extra_columns_str = opts.extra_columns
    extra_columns = {}
    if extra_columns_str is not None:
        kws = extra_columns_str.split(',')
        for kw in kws:
            k, v = kw.split(':', maxsplit=1)
            extra_columns[k] = v

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
    em_conll = ('emconll.converter', 'EmCoNLL', 'CoNLL-U converter',
                (opts.print_header, opts.force_id, opts.add_space_after_no, extra_columns),
                {'source_fields': {'form'}, 'target_fields': []})
    tools = [(em_conll, ('conll', 'emCoNLL'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, opts.conllu_comments))


if __name__ == '__main__':
    main()
