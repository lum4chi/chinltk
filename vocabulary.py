#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>
import cPickle

class Vocabulary:
    #TODO IDs can be inconsistent if using manual AND automatic mapping.
    """
        Provide a way to organize words of a context and various
        related infos. Words should be loaded only through provide methods.
        Optional known synonyms should not appear in initial loading
        and mapped later.
    """
    def __init__(self):
        self._dictionary = dict() # map every word with an ID (auto-increment of user defined)
        self.synonyms = dict() # map a word with its known "normal-form" word

    def __getitem__(self, word):
        return self._dictionary[word]

    def __len__(self):
        return len(self._dictionary)

    def add_word(self, word, ID=None):
        if word not in self._dictionary:
            if ID is not None:
                self._dictionary[word] = ID
            else:
                self._dictionary[word] = len(self._dictionary)
        else:
            print 'Word already present. Skipping', word

    def add_words(self, words, IDs=None):
        """
            Load a vocabulary with defined words (optionally mapped
            with an user-defined ID: if not, auto-increment)
        :param words: list of words
        :param IDs: list of IDs, same order/length of words
        """
        if IDs is not None:
            assert len(words) == len(IDs)
            for w, i in zip(words, IDs): self.add_word(w, i)
        else:
            for i, w in enumerate(words, len(self._dictionary)): self.add_word(w, i)

    def add_synonyms(self, word, syns):
        """ Every synonym is mapped to its normal word """
        for s in syns: self.synonyms[s] = word

    def main_synonym(self, word):
        """  If word is a known synonym, it is replaced with is normal-form """
        return word if word not in self.synonyms else self.synonyms[word]

    def words_filter(self, words, filler=None, process_synonyms=True):
        """ Remove words with chosen filler if not present in Vocabulary.
        :param filler: if specified, a filtered words is returned as value specified here
        """
        if process_synonyms:
            if filler is not None:
                return [self.main_synonym(w) if self.main_synonym(w) in self._dictionary else filler for w in words]
            else:
                return [self.main_synonym(w) for w in words if self.main_synonym(w) in self._dictionary]
        else:
            if filler is not None:
                return [w if w in self._dictionary else filler for w in words]
            else:
                return [w for w in words if w in self._dictionary]

    def save(self, fname):
        # TODO fare un file con SOLO dati per ottimizzare lo spazio
        return cPickle.dump(self, open(fname, 'wb'))

    @staticmethod
    def load(fname):
        # TODO fare un file con SOLO dati per ottimizzare lo spazio
        return cPickle.load(open(fname, 'rb'))
