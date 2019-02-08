# -*- coding: utf-8 -*-
"""
Conversion between inner Mystem format and Universal Dependencies
(http://universaldependencies.org/ru/pos/all.html)
https://tech.yandex.ru/mystem/doc/grammemes-values-docpage/

Known issues:
TODO
"""
from __future__ import absolute_import, unicode_literals
from copy import deepcopy

from russian_tagsets import converters
import re

class Tag14(object):

    GRAM_MAP = {
        '_POS': {
            'A': 'ADJ', # прилагательное
            # 'ADJS': 'ADJ',
            'ADV': 'ADV', # наречие
            'APRO': 'DET', #?? местоимение-прилагательное
            'ADVPRO': 'DET', #?? местоименное наречие
            'CONJ': 'CONJ', #  союз
            'V': 'VERB', # глагол,
            'COM': 'X', # ?? 
            # 'INFN': 'VERB',
            'INTJ': 'INTJ', # междометие
            'S': 'NOUN', # существительное
            'SPRO': 'PRON', # местоимение-существительное
            'NUM': 'NUM', # числительное
            'ANUM': 'NUM', # числительное-прилагательное
            # 'NUMB': 'NUM', 
            # 'PART': 'PRCL',
            # 'PNCT': 'PUNCT',
            'PART': 'PART', # частица
            'PR': 'ADP', # предлог
            # 'PRTF': 'VERB',
            # 'PRTS': 'VERB',
            # 'VERB': 'VERB',
        },
        'Animacy': { # 
            'од': 'Anim',
            'неод': 'Inan',
        },
        'Aspect': {
            'несов': 'Imp',
            'сов': 'Perf',
        },
        'Case': { # 
            'твор': 'Ins',
            'вин': 'Acc',
            'дат': 'Dat',
            'род': 'Gen',
            'парт': 'Gen',
            # 'gent': 'Gen',
            'местн': 'Loc',
            'пр': 'Loc',
            'им': 'Nom',
            'зват': 'Nom',
        },
        'Degree': { # 
            'срав': 'Cmp',
            'прев': 'Sup',
        },
        'Gender': { #
            'жен': 'Fem',
            'муж': 'Masc',
            'сред': 'Neut',
        },
        'Mood': { # ??
            'пов': 'Imp',
            'изъяв': 'Ind'
        },
        'Number': { # 
            'мн': 'Plur',
            'ед': 'Sing',
        },
        'NumForm': {
            'NUMB': 'Digit',
        },
        'Person': { # 
            '1-л': '1',
            '2-л': '2',
            '3-л': '3',
        },
        'Tense': { # 
            'непрош': 'Fut',
            'прош': 'Past',
            'наст': 'Pres',
        },
        'Variant': {
            'ADJS': 'Brev',
            'PRTS': 'Brev',
        },
        'Subcat': {
            'нп': 'Intr',
            'пе': 'Tran'
        }
        ,
        'VerbForm': {
            'инф': 'Inf',
            'деепр': 'Grnd',
            'прич': 'Part',
        },
        'Voice': { #
            'действ': 'Act',
            'страд': 'Pass',
        },
        'Style': {
            'редк': 'Rare',
            'обсц': 'Vulg',
            'устар': 'Arch',
            'разг': 'Slng'
        }
    }

    def __init__(self, oc_tag):
        self.pos = 'X'
        self.grammemes = dict()
        self.unmatched = set()
        self._fill_from_oc(oc_tag)

    def _postprocess(self):
        while len(self.unmatched) > 0:
            gram = self.unmatched.pop()

            if gram in ('имя', 'фам', 'гео', 'отч'):
                self.pos = 'PROPN'
            # elif gram == 'сокр':
            #     self.pos = 'NOUN' # ?? PROPN?

    def _fill_one_gram_oc(self, gram):
        match = False
        for categ, gmap in sorted(self.GRAM_MAP.items()):
            if gram in gmap:
                if categ == '_POS':
                    self.pos = gmap[gram]
                    match = True
                else:
                    self.grammemes[categ] = gmap[gram]
                    match = True

        if not match:
            self.unmatched.add(gram)

    def _fill_from_oc(self, oc_tag):
        grams = re.split('\W', oc_tag)
        # print(oc_tag, grams)
        # grams = oc_tag.replace(' ', ',').split(',')
        for g in grams:
            self._fill_one_gram_oc(g)
        self._postprocess()

    def __str__(self):
        grams = '|'.join("{}={}".format(c, v) for c, v in sorted(self.grammemes.items()))
        return "{} {}".format(self.pos, grams if grams else '_')



class Tag20(Tag14):
    GRAM_MAP = deepcopy(Tag14.GRAM_MAP)
    # http://universaldependencies.org/v2/postags.html
    GRAM_MAP['_POS']['CONJ'] = 'CCONJ'
    # http://universaldependencies.org/v2/features.html
    GRAM_MAP['VerbForm']['деепр'] = 'Conv'
    GRAM_MAP['Abbr'] = {'сокр': 'Yes'}


def to_ud14(oc_tag, word=None):
    tag = Tag14(oc_tag)
    return str(tag)


def to_ud20(oc_tag, word=None):
    tag = Tag20(oc_tag)
    return str(tag)

converters.add('mystem', 'ud14', to_ud14)
converters.add('mystem', 'ud20', to_ud20)
