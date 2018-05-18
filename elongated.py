#!/usr/bin/env python
"""Remove consecutive duplicate characters unless inside a known word.
"""
import fileinput
import re
import sys
from itertools import groupby, product
import enchant # $ pip install pyenchant

tripled_words = set(['ballless', 'belllike', 'crosssection', 'crosssubsidize', 'jossstick', 'shellless','aaadonta', 'flying','jibbboom', 'peeent', 'freeer', 'freeest', 'ishiii', 'frillless', 'wallless', 'laparohysterosalpingooophorectomy', 'goddessship', 'countessship', 'duchessship', 'governessship', 'hostessship', 'vertuuus','crossselling','crossshaped','crossstitch','fulllength','illlooking','massspectrometry','missstay','offform','palllike','pressstud','smallleaved','shellless','shelllike','stilllife','threeedged'])


def remove_consecutive_dups(s):
	# return number of letter >= 1
    # return re.sub(r'(?i)(.)\1+', r'\1', s)
	# return number of letter >= 2
    return re.sub(r'(?i)(.)\1+', r'\1\1', s)

def all_consecutive_duplicates_edits(word, max_repeat=float('inf')):
    chars = [[c*i for i in range(min(len(list(dups)), max_repeat), 0, -1)]
             for c, dups in groupby(word)]
    return map(''.join, product(*chars))

def has_long(sentence):
    elong = re.compile("([a-zA-Z])\\1{2,}")
    return bool(elong.search(sentence))

if __name__ == '__main__':

	words = enchant.Dict("en")
	is_known_word = words.check

	sentence = "that's good if you keep the bees safe. happy life. cooooll. let's play fooooootballll"

	# print has_long(sentence)
	input_w = "fooooootballll"
	if has_long(sentence):
		if not any(input_w in x for x in tripled_words):
			print remove_consecutive_dups(input_w),is_known_word(remove_consecutive_dups(input_w)), words.suggest(remove_consecutive_dups(input_w))
			words_map = all_consecutive_duplicates_edits(input_w)

			print "-----------------------------------------\n"
			for word in words_map:
				print word, is_known_word(word)
				if is_known_word(word):
					print words.suggest(word)

	# for line in fileinput.input(inplace=False):
	#     #NOTE: unnecessary work, optimize if needed
	#     output = [next((e for e in all_consecutive_duplicates_edits(s)
	#                     if e and is_known_word(e)), remove_consecutive_dups(s))
	#               for s in re.split(r'(\W+)', line)]
	#     sys.stdout.write(''.join(output))