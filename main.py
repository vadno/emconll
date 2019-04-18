#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

# oszlopnevek megfeleltetései (deps és misc hiányzik az emtsvből)
col_mapper = {'id': 'ID',
              'form': 'FORM',
              'lemma': 'LEMMA',
              'upostag': 'UPOS',
              'xpostag': 'XPOS',
              'feats': 'FEATS',
              'head': 'HEAD',
              'deprel': 'DEPREL'
              }

# a conll oszlopnevek sorrendben
conll = ['ID', 'FORM', 'LEMMA', 'UPOS', 'XPOS', 'FEATS', 'HEAD', 'DEPREL', 'DEPS', 'MISC']


def read_file(filename):
    """
    beolvassa az emtsv kimenetét
    kinyeri az oszlopneveket
    listába elrakja a sorok tartalmát (amelyek szintén listák)
    :param filename: a beolvasandó fájl neve (emtsv kimenete)
    :return: kinyert oszlopnevek, sorok listája
    """

    with open(filename, 'r') as inf:
        # első sor a fejléc az oszlopnevekkel
        header = inf.readline().strip().split()
        # kinyerem az oszlopszámokat a header sorrendjéből
        col_name = {i: header[i] for i in range(0, len(header))}

        cols = []

        for line in inf:
            cols.append(line.strip().split('\t'))

    return col_name, cols


def map_cols(cols):
    """
    az emtsv oszlopneveit megfelelteti a conll oszlopneveknek
    :param cols: emtsv oszlopnevek dictben (kulcs: oszlopszám, érték: oszlopnév)
    :return:
    """

    for c in cols:
        if cols[c] in col_mapper:
            cols[c] = col_mapper[cols[c]]


def rotate(col_name, cols):
    """
    a conll oszlopoknak megfelelő dictekbe teszi a sorok tartalmát
    :param col_name: oszlopnevek, ahol a conll-nek megfeleltethető nevek mappelve vannak a conll-re
    :param cols: sorok
    :return: dictek listája, ahol a dictben az egyes mezők a conll oszlopoknak vannak megfeleltetve
    """

    conll_lines = list()

    for line in cols:
        if len(line) > 1:
            line_dict = dict()
            for c in col_name:
                line_dict[col_name[c]] = line[c]
            conll_lines.append(line_dict)
        else:
            conll_lines.append([])

    return conll_lines


def print_conll(conll_lines):
    """
    kinyomtatja a jól formázott conll fájlt
    :param conll_lines: a dictekben rendezett sorok, amiből már nyotmatható a megfelelő sorrend
    :return:
    """

    with open('vizilo.conll', 'w') as ouf:

        print('\t'.join(conll), file=ouf)

        for line in conll_lines:
            if len(line) > 1:
                to_print = list()
                for col in conll:
                    if col not in line:
                        to_print.append('_')
                    else:
                        to_print.append(line[col])
                print('\t'.join(to_print), file=ouf)
            else:
                print('', file=ouf)


def main():
    # beolvassuk az emtsv kimenetet, kinyerjük az oszlopneveket és oszlopszámokat is
    col_name, cols = read_file(sys.argv[1])
    # az oszlopneveket megfeleltetjük a conll-nek
    map_cols(col_name)
    # az oszlopokat conll sorrendezzük
    conll_lines = rotate(col_name, cols)
    # kiírjuk a connl fájlt
    print_conll(conll_lines)

    # TODO conll validátort be lehetne illeszteni a nyomtatás elé

if __name__ == "__main__":
    main()
