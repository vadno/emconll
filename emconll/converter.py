#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-


class EmCoNLL:
    pass_header = False

    def __init__(self, print_header=False, force_id=False, add_space_after_no=False, extra_columns=None,
                 source_fields=None, target_fields=None):
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

        if extra_columns is not None:  # Keys are unique for each dict, but values may duplicate!
            if len(self._col_mapper.keys() & extra_columns.keys()) > 0 or \
                    len(set(self._col_mapper.values()) & set(extra_columns.values())) > 0 or \
                    len(set(extra_columns.values())) < len(extra_columns.values()):
                raise ValueError(f'Some extra_column input or output name is duplicated:'
                                 f' {self._col_mapper} and {extra_columns} !')
            self._col_mapper.update(extra_columns)
        self._print_header = print_header
        self._force_id = force_id
        self._add_id = self._dummy_fun
        self._add_space_after_no = add_space_after_no
        self._add_space_after_no_fun = self._dummy_fun
        self._ws_after_column_no = -1
        self._sentence_count = 0

        # Field names for e-magyar TSV
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

    @staticmethod
    def _dummy_fun(_, new_line):
        return new_line

    def _add_space_after_no_real_fun(self, orig_line, new_line):
        if orig_line[self._ws_after_column_no] == '""':
            misc = 'SpaceAfter=No'
        else:
            misc = '_'
        new_line[9] = misc  # wsafter -> misc
        return new_line

    @staticmethod
    def _add_id_fun(i, new_line):
        new_line[0] = str(i)
        return new_line

    def process_sentence(self, sen, field_names):
        """
        Reorder the needed fields and put _ when a mandatory field missing (eg. not created yet)
        :param sen: The sentence splitted to tokens and fields
        :param field_names: The name of the fields mapped to the column indices
        :return: A generator yields the output line-by-line
        """
        self._sentence_count += 1

        if self._print_header and self._sentence_count == 1:
            yield self._col_mapper.values()

        for i, line in enumerate(sen, start=1):
            new_line = [line[col] if col != '_' else '_' for col in field_names]
            new_line = self._add_id(i, new_line)
            new_line = self._add_space_after_no_fun(line, new_line)
            yield new_line

    def prepare_fields(self, field_names):
        """
        Map the mandatory emtsv field names to the CoNLL names tied to the current indices
        :param field_names: emtsv header
        :return: (list) The "mapping" of the mandatory CoNLL field names to the current indices
        """

        fields_nums = [field_names.get(emtsv_name, '_') for emtsv_name in self._col_mapper.keys()]
        if self._add_space_after_no and fields_nums[9] == '_' and field_names.get('wsafter') is not None:
            self._add_space_after_no_fun = self._add_space_after_no_real_fun
            self._ws_after_column_no = field_names['wsafter']
        if self._force_id and fields_nums[0] == '_':
            self._add_id = self._add_id_fun

        return fields_nums
