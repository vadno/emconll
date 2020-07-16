#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class EmCoNLL:
    pass_header = False

    def __init__(self, source_fields=None, target_fields=None):
        self._col_mapper = {'id': 'ID',
                            'form': 'FORM',
                            'lemma': 'LEMMA',
                            'upostag': 'UPOS',
                            'xpostag': 'XPOS',
                            'feats': 'FEATS',
                            'head': 'HEAD',
                            'deprel': 'DEPREL'
                            }

        # The CoNLL columns in order
        self._conll = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    def process_sentence(self, sen, field_names):
        """
        Reorder the needed fields and put _ when a mandatory field missing (eg. not created yet)
        :param sen: The sentence splitted to tokens and fields
        :param field_names: The name of the fields mapped to the column indices
        :return: A generator yields the output line-by-line
        """

        for line in sen:
            new_line = (line[field_names[col]] if col in field_names else '_'
                        for col in self._conll)
            yield new_line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: Mapping of the mandatory CoNLL field names to the current indices
        """

        return {self._col_mapper[emtsv_name]: col_num for col_num, emtsv_name in field_names.items()
                if emtsv_name in self._col_mapper}
