#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>
import cPickle
from itertools import izip_longest


class Vocabulary:
    """
        Provide a way to organize words and provide translation to a main
        dictionary of terms.
    """

    def __init__(self):
        self.word2id = dict()   # map word with an optional ID
        self.id2word = dict()   # map back id -> main word
        self.synonyms = dict()  # map a word with its known "normal-form" word

    def __getitem__(self, word):
        return self.word2id[word]

    def __len__(self):
        return len(self.word2id)

    def add_word(self, word, ID=None):
        if word not in self.word2id:
            self.word2id[word] = ID
        else:
            print 'Word already present. Skipping', word

    def add_words(self, words, IDs=list(), fillvalue=None):
        """
            Load a vocabulary with defined words (optionally mapped
            with an user-defined ID)
        :param words: list of words
        :param IDs: list of IDs, same order/length of words
        """
        for w, i in izip_longest(words, IDs, fillvalue=fillvalue):
            self.add_word(w, i)

    def add_synonyms(self, word, syns):
        """ Every synonym is mapped to its normal word """
        for s in syns: self.synonyms[s] = word

    def main_synonym(self, word):
        """  If word is a known synonym, it is replaced with is normal-form """
        return word if word not in self.synonyms else self.synonyms[word]

    def word_filter(self, word, filler=None, word2id=False):
        """
            Remove word or replace it with chosen filler if not present in
            Vocabulary.
        :param word: term to filter
        :param filler: if specified, a filtered words is returned as this value
        :param word2id: if True: words are mapped to user-defined id
        :return:
        """
        w = self.main_synonym(word)
        if word2id:
            w = self.word2id[w] if w in self.word2id else filler
        else:
            w = w if w in self.word2id else filler
        if w is not None: return w

    def words_filter(self, words, filler=None, word2id=False):
        filtered = [self.word_filter(w, filler, word2id) for w in words]
        return [w for w in filtered if w is not None]

    def id_filter(self, _id, filler=None, id2word=False):
        """
            Remove id or replace it with chosen filler if not present in
            Vocabulary.
        :param _id: id to filter
        :param filler: if specified, a filtered id is returned as this value
        :param id2word: if True: id are mapped back to word
        :return:
        """
        if len(self.id2word) == 0:  # Greedy build
            self.id2word = {v: k for k, v in self.word2id.items()
                            if v is not None}
        if id2word:
            _id = self.id2word[_id] if _id in self.id2word else filler
        else:
            _id = _id if _id in self.id2word else filler
        if _id is not None: return _id

    def ids_filter(self, ids, filler=None, id2word=False):
        filtered = [self.id_filter(_id, filler, id2word) for _id in ids]
        return [_id for _id in filtered if _id is not None]

    def save(self, fname):
        return cPickle.dump(self, open(fname, 'wb'))

    @staticmethod
    def load(fname):
        return cPickle.load(open(fname, 'rb'))
