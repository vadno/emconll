#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class EmCoNLL:
    pass_header = False

    def __init__(self, source_fields=None, target_fields=None):
        # From emtsv format to CoNLL-U (in CoNLL-U order)
        self._col_mapper = {'id': 'ID',
                            'form': 'FORM',
                            'lemma': 'LEMMA',
                            'upostag': 'UPOS',
                            'xpostag': 'XPOS',
                            'feats': 'FEATS',
                            'head': 'HEAD',
                            'deprel': 'DEPREL',
                            'deps': 'DEPS',
                            'misc': 'MISC'
                            }

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    @staticmethod
    def process_sentence(sen, field_names):
        """
        Reorder the needed fields and put _ when a mandatory field missing (eg. not created yet)
        :param sen: The sentence splitted to tokens and fields
        :param field_names: The name of the fields mapped to the column indices
        :return: A generator yields the output line-by-line
        """

        for line in sen:
            new_line = (line[col] if col != '_' else '_' for col in field_names)
            yield new_line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: (list) The "mapping" of the mandatory CoNLL field names to the current indices
        """

        return [field_names.get(emtsv_name, '_') for emtsv_name in self._col_mapper.keys()]
