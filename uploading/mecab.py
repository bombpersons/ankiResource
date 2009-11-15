# -*- coding: utf-8 -*-
# taken from anki japanese plugin source code
# permission pending

import sys, os, platform, re, subprocess

# disable to use kakasi only
USE_MECAB=True

modelTag = "Japanese"
srcField = "Expression"
dstField = "Reading"

if USE_MECAB:
    kakasiCmd = ["kakasi", "-isjis", "-osjis", "-u", "-JH", "-KH"]
else:
    kakasiCmd = ["kakasi", "-isjis", "-osjis", "-u", "-JH", "-p"]
mecabCmd = ["mecab", '--node-format=%m[%f[7]] ', '--eos-format=\n',
            '--unk-format=%m[] ']

def escapeText(text):
    # strip characters that trip up kakasi/mecab
    text = text.replace("\n", " ")
    text = text.replace(u'\uff5e', "~")
    text = re.sub("<br( /)?>", "---newline---", text)
    text = text.replace("---newline---", "<br>")
    return text

si = None

# Mecab
##########################################################################

class MecabController(object):

    def __init__(self):
        self.mecab = None

    def ensureOpen(self):
        if not self.mecab:
            try:
                self.mecab = subprocess.Popen(
                    mecabCmd, bufsize=-1, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, startupinfo=si)
            except OSError:
                raise Exception(_("Please install mecab"))

    def parse_words(self, expr):
        self.ensureOpen()
        expr = escapeText(expr)
        self.mecab.stdin.write(expr.encode("euc-jp", "ignore")+'\n')
        self.mecab.stdin.flush()
        expr = unicode(self.mecab.stdout.readline().rstrip('\r\n'), "euc-jp")
        words = []
        for node in expr.split(" "):
            if not node:
                break
            (kanji, reading) = re.match("(.+)\[(.*)\]", node).groups()
            # punctuation
            if kanji in u"。、.,?!":
            	continue
        	# number
            if kanji in u"一二三四五六七八九十０１２３４５６７８９" or kanji in "0123456789":
                continue
            # same as reading
            if kanji == kakasi.reading(reading) or kanji == reading:
                if len(kanji) == 1:
                    continue
                else:
		            words.append((kanji))
                continue
            
            words.append(kanji)

        #words = set(words)
        for word in words:
            print word


# Kakasi
##########################################################################

class KakasiController(object):

    def __init__(self):
        self.kakasi = None

    def setup(self):
        if sys.platform == "win32":
            dir = WIN32_READING_DIR
            os.environ['PATH'] += (";%s\\kakasi\\bin" % dir)
            os.environ['ITAIJIDICT'] = ("%s\\kakasi\dic\\itaijidict" %
                                        dir)
            os.environ['KANWADICT'] = ("%s\\kakasi\\dic\\kanwadict" % dir)
        elif sys.platform.startswith("darwin"):
            dir = os.path.dirname(os.path.abspath(__file__))
            os.environ['PATH'] += ":" + dir + "/osx/kakasi"
            os.environ['ITAIJIDICT'] = dir + "/osx/kakasi/itaijidict"
            os.environ['KANWADICT'] = dir + "/osx/kakasi/kanwadict"
            os.chmod(dir + "/osx/kakasi/kakasi", 0755)

    def ensureOpen(self):
        if not self.kakasi:
            self.setup()
            try:
                self.kakasi = subprocess.Popen(
                    kakasiCmd, bufsize=-1, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, startupinfo=si)
            except OSError:
                raise Exception(_("Please install kakasi"))

    def reading(self, expr):
        self.ensureOpen()
        expr = escapeText(expr)
        self.kakasi.stdin.write(expr.encode("sjis", "ignore")+'\n')
        self.kakasi.stdin.flush()
        res = unicode(self.kakasi.stdout.readline().rstrip('\r\n'), "sjis")
        return res

kakasi = None
mecab = None

kakasi = KakasiController()
mecab = MecabController()
mecab.ensureOpen()

# Tests
##########################################################################

if __name__ == "__main__" and False:
    expr = u"カリン、自分でまいた種は自分で刈り取れ"
    print expr
    mecab.parse_words(expr)
    expr = u"昨日、林檎を2個買った。"
    print expr
    mecab.parse_words(expr)
    expr = u"真莉、大好きだよん＾＾"
    print expr
    mecab.parse_words(expr)
    expr = u"彼２０００万も使った。"
    print expr
    mecab.parse_words(expr)
    expr = u"彼二千三百六十円も使った。"
    print expr
    mecab.parse_words(expr)
    expr = u"千葉"
    print expr
    mecab.reading(expr)
