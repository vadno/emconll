#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

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


def read_file(input_iterator):  # TODO XTSV-vel megoldani: Ezt az XTSV csinálja, nem kell itt implementálni.
    """
    beolvassa az emtsv kimenetét
    kinyeri az oszlopneveket
    listába elrakja a sorok tartalmát (amelyek szintén listák)
    :param input_iterator: a beolvasandó stream neve (emtsv kimenete)
    :return: kinyert oszlopnevek, sorok listája
    """
    # első sor a fejléc az oszlopnevekkel
    header = input_iterator.readline().strip().split()
    # kinyerem az oszlopszámokat a header sorrendjéből
    col_name = {i: col for i, col in enumerate(header)}
    lines = [line.strip().split('\t') for line in input_iterator]  # TODO: Itt az egész a memóriában van! Veszélyes!
    #  Ebből látszik, hogy külön kell a headert beolvasni a contenttől, mert a content egy iterátor kell, hogy legyen.
    return col_name, lines


def map_cols(cols):  # TODO XTSV-vel megoldani: prepare_fields()
    """
    az emtsv oszlopneveit megfelelteti a conll oszlopneveknek
    :param cols: emtsv oszlopnevek dictben (kulcs: oszlopszám, érték: oszlopnév)
    :return:
    """

    for c in cols:
        if cols[c] in col_mapper:
            cols[c] = col_mapper[cols[c]]


def rotate(col_name, lines):  # TODO: Ezt a print_conll()-en belülről kellene hívni, mert amúgy fölöslegs az XTSV miatt.
    """
    a conll oszlopoknak megfelelő dictekbe teszi a sorok tartalmát
    :param col_name: oszlopnevek, ahol a conll-nek megfeleltethető nevek mappelve vannak a conll-re
    :param lines: sorok
    :return: dictek iterátora, ahol a dictben az egyes mezők a conll oszlopoknak vannak megfeleltetve
    """

    for line in lines:
        line_dict = dict()
        if len(line) > 1:
            line_dict = {col_name[c]: line[c] for c in col_name}
        yield line_dict  # Így egyszrre egy sorral foglalkozunk, nincs memória korlát.


def print_conll(conll_lines):  # TODO: Ő lesz a fő függvény: process_sentence()
    """
    kinyomtatja a jól formázott conll fájlt
    :param conll_lines: a dictekben rendezett sorok, amiből már nyotmatható a megfelelő sorrend
    :return: egy generátor, ami soronként előállítja a kimeneti fájlt
    """

    # nincs header a conll-u-ban!
    # yield '{0}\n'.format('\t'.join(conll))

    for line in conll_lines:
        if len(line) > 1:
            to_print = list()
            for col in conll:
                if col not in line:
                    to_print.append('_')
                else:
                    to_print.append(line[col])
            yield '{0}\n'.format('\t'.join(to_print))
        else:
            yield '\n'


def main():
    # beolvassuk az emtsv kimenetet, kinyerjük az oszlopneveket és oszlopszámokat is
    with open(sys.argv[1], encoding='UTF-8') as inf:
        col_name, lines = read_file(inf)
    # az oszlopneveket megfeleltetjük a conll-nek
    map_cols(col_name)
    # az oszlopokat conll sorrendezzük
    conll_lines = rotate(col_name, lines)
    # kiírjuk a connl fájlt
    with open('vizilo.conll', 'w', encoding='UTF-8') as ouf:
        ouf.writelines(print_conll(conll_lines))

if __name__ == '__main__':
    main()
