#!/usr/bin/python
# coding=utf-8

import MeCab

def j2u(expr):
	return unicode(expr, "euc-jp")

t = MeCab.Tagger()

def is_real_word(mfs):
	if j2u(mfs[1]) == u"数" or j2u(mfs[0]) == u"助詞" or j2u(mfs[0]) == u"助動詞" or j2u(mfs[0]) == u"記号":
		return False
	else:
		return True

def parse_print(sentence):
	#deconjugates each word in sentence and prints with o for "real word" and x otherwise
	sentence = sentence.encode("euc-jp", "ignore")
	print unicode(sentence, "euc-jp")
	m = t.parseToNode (sentence)
	m = m.next	#clears the first entry
	while m:
		mfs = m.feature.split(",")
		if j2u(mfs[0]) != "BOS/EOS":
			if is_real_word(mfs):
				print "o",
			else:
				print "x",
			print unicode(m.surface + "\t\t" + m.feature, "euc-jp")
		m = m.next
		
def parse(sentence):
	#searches for words in sentence,deconjugates and returns them
	sentence = sentence.encode("euc-jp", "ignore")
	m = t.parseToNode (sentence)
	m = m.next	#clears the first entry
	words = []
	while m:
		mfs = m.feature.split(",")
		if j2u(mfs[0]) != "BOS/EOS" and is_real_word(mfs):
			words.append(j2u(m.surface))
		m = m.next
	return words

def print_in(l):
	for word in l:
		print word,
	print "\n",
		
if __name__ == "__main__":
	parse_print(u"カリン、自分でまいた種は自分で刈り取れ")
	parse_print(u"昨日、林檎を2個買った。")
	parse_print(u"真莉、大好きだよん＾＾")
	parse_print(u"彼２０００万も使った。")
	parse_print(u"彼二千三百六十円も使った。")
	parse_print(u"千葉")
	
	print_in(parse(u"カリン、自分でまいた種は自分で刈り取れ"))
	print_in(parse(u"昨日、林檎を2個買った。"))
	print_in(parse(u"真莉、大好きだよん＾＾"))
	print_in(parse(u"彼２０００万も使った。"))
	print_in(parse(u"彼二千三百六十円も使った。"))
	print_in(parse(u"千葉"))
