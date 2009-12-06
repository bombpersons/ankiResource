# coding=utf-8

import urllib, string, os, json


def get_from_smart_fm(word):
	Url = "http://api.smart.fm/sentences/matching/%s?language=ja&format=json" % word.encode('utf-8')
	opened_url = urllib.urlopen(Url)
	json_text =  opened_url.readlines()[0]
	json_parsed = json.loads(json_text)

	return [sentence["text"] for sentence in json_parsed]
