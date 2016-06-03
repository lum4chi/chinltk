#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Francesco Lumachi <francesco.lumachi@gmail.com>
import nltk, string

def words(text):
    """ Tokenize by word AND removed punctuation token """
    return [w for w in nltk.word_tokenize(text.lower()) if w not in string.punctuation]

def filter_stopwords(words):
    """ Filter stopwords from a list of words """
    stopwords = set(nltk.corpus.stopwords.words('english')) # push this in comprehension slow A LOT!
    return [w for w in words if w.lower() not in stopwords]

def filter_words(words, filters):
    """ Filter words from a list of filters """
    filters = set(filters)
    return [w for w in words if w.lower() not in filters]

def biwords(text):
    """ Iterate over biword """
    word_list = words(text)
    first, second = iter(word_list), iter(word_list[1:])
    return [' '.join([f, s]) for f, s in zip(first, second)] # -> 'first second'
