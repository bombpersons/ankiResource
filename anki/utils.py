# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""\
Miscellaneous utilities
==============================
"""
__docformat__ = 'restructuredtext'

import re, os, random, time, types

try:
    import hashlib
    md5 = hashlib.md5
except ImportError:
    import md5
    md5 = md5.new

from anki.db import *
from anki.lang import _, ngettext
import locale, sys

if sys.version_info[1] < 5:
    def format_string(a, b):
        return a % b
    locale.format_string = format_string

# Time handling
##############################################################################

timeTable = {
    "years": lambda n: ngettext("%s year", "%s years", n),
    "months": lambda n: ngettext("%s month", "%s months", n),
    "days": lambda n: ngettext("%s day", "%s days", n),
    "hours": lambda n: ngettext("%s hour", "%s hours", n),
    "minutes": lambda n: ngettext("%s minute", "%s minutes", n),
    "seconds": lambda n: ngettext("%s second", "%s seconds", n),
    }

afterTimeTable = {
    "years": lambda n: ngettext("%s year<!--after>", "%s years<!--after>", n),
    "months": lambda n: ngettext("%s month<!--after>", "%s months<!--after>", n),
    "days": lambda n: ngettext("%s day<!--after>", "%s days<!--after>", n),
    "hours": lambda n: ngettext("%s hour<!--after>", "%s hours<!--after>", n),
    "minutes": lambda n: ngettext("%s minute<!--after>", "%s minutes<!--after>", n),
    "seconds": lambda n: ngettext("%s second<!--after>", "%s seconds<!--after>", n),
    }

shortTimeTable = {
    "years": "%sy",
    "months": "%sm",
    "days": "%sd",
    "hours": "%sh",
    "minutes": "%sm",
    "seconds": "%ss",
    }

def fmtTimeSpan(time, pad=0, point=0, short=False, after=False):
    "Return a string representing a time span (eg '2 days')."
    (type, point) = optimalPeriod(time, point)
    time = convertSecondsTo(time, type)
    if short:
        fmt = shortTimeTable[type]
    else:
        if after:
            fmt = afterTimeTable[type](_pluralCount(round(time, point)))
        else:
            fmt = timeTable[type](_pluralCount(round(time, point)))
    timestr = "%(a)d.%(b)df" % {'a': pad, 'b': point}
    return locale.format_string("%" + (fmt % timestr), time)

def fmtTimeSpanPair(time1, time2, short=False, after=False):
    (type, point) = optimalPeriod(time1, 0)
    time1 = convertSecondsTo(time1, type)
    time2 = convertSecondsTo(time2, type)
    # a pair is always  should always be read as plural
    if short:
        fmt = shortTimeTable[type]
    else:
        if after:
            fmt = afterTimeTable[type](2)
        else:
            fmt = timeTable[type](2)
    timestr = "%(a)d.%(b)df" % {'a': pad, 'b': point}
    finalstr = "%s-%s" % (
        locale.format_string('%' + timestr, time1),
        locale.format_string('%' + timestr, time2),)
    return fmt % finalstr

def optimalPeriod(time, point):
    if abs(time) < 60:
        type = "seconds"
        point -= 1
    elif abs(time) < 3599:
        type = "minutes"
    elif abs(time) < 60 * 60 * 24:
        type = "hours"
    elif abs(time) < 60 * 60 * 24 * 30:
        type = "days"
    elif abs(time) < 60 * 60 * 24 * 365:
        type = "months"
        point += 1
    else:
        type = "years"
        point += 1
    return (type, max(point, 0))

def convertSecondsTo(seconds, type):
    if type == "seconds":
        return seconds
    elif type == "minutes":
        return seconds / 60.0
    elif type == "hours":
        return seconds / 3600.0
    elif type == "days":
        return seconds / 86400.0
    elif type == "months":
        return seconds / 2592000.0
    elif type == "years":
        return seconds / 31536000.0
    assert False

def _pluralCount(time):
    if round(time, 1) == 1:
        return 1
    return round(time, 1)

# Locale
##############################################################################

def fmtPercentage(float_value, point=1):
    "Return float with percentage sign"
    fmt = '%' + "0.%(b)df" % {'b': point}
    return locale.format_string(fmt, float_value) + "%"

def fmtFloat(float_value, point=1):
    "Return a string with decimal separator according to current locale"
    fmt = '%' + "0.%(b)df" % {'b': point}
    return locale.format_string(fmt, float_value)

# HTML
##############################################################################

def stripHTML(s):
    s = re.sub("(?s)<style.*?>.*?</style>", "", s)
    s = re.sub("<.*?>", "", s)
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    return s

def tidyHTML(html):
    "Remove cruft like body tags and return just the important part."
    # contents of body - no head or html tags
    html = re.sub(u".*<body.*?>(.*)</body></html>",
                  "\\1", html.replace("\n", u""))
    # strip superfluous Qt formatting
    html = re.sub(u"margin-top:\d+px; margin-bottom:\d+px; margin-left:\d+px; "
                  "margin-right:\d+px; -qt-block-indent:0; "
                  "text-indent:0px;", u"", html)
    html = re.sub(u"-qt-paragraph-type:empty;", u"", html)
    # strip leading space in style statements, and remove if no contents
    html = re.sub(u'style=" ', u'style="', html)
    html = re.sub(u' style=""', u"", html)
    # convert P tags into SPAN and/or BR
    html = re.sub(u'<p( style=.+?)>(.*?)</p>', u'<span\\1>\\2</span><br>', html)
    html = re.sub(u'<p>(.*?)</p>', u'\\1<br>', html)
    html = re.sub(u'<br>$', u'', html)
    return html

# IDs
##############################################################################

def genID(static=[]):
    "Generate a random, unique 64bit ID."
    # 23 bits of randomness, 41 bits of current time
    # random rather than a counter to ensure efficient btree
    t = long(time.time()*1000)
    if not static:
        static.extend([t, {}])
    else:
        if static[0] != t:
            static[0] = t
            static[1] = {}
    while 1:
        rand = random.getrandbits(23)
        if rand not in static[1]:
            static[1][rand] = True
            break
    x = rand << 41 | t
    # turn into a signed long
    if x >= 9223372036854775808L:
        x -= 18446744073709551616L
    return x

def hexifyID(id):
    if id < 0:
        id += 18446744073709551616L
    return "%x" % id

def dehexifyID(id):
    id = int(id, 16)
    if id >= 9223372036854775808L:
        id -= 18446744073709551616L
    return id

def ids2str(ids):
    """Given a list of integers, return a string '(int1,int2,.)'

The caller is responsible for ensuring only integers are provided.
This is safe if you use sqlite primary key columns, which are guaranteed
to be integers."""
    return "(%s)" % ",".join([str(i) for i in ids])

# Tags
##############################################################################

def parseTags(tags):
    "Parse a string and return a list of tags."
    tags = re.split(" |, ?", tags)
    return [t.strip() for t in tags if t.strip()]

def joinTags(tags):
    return u" ".join(tags)

def canonifyTags(tags):
    "Strip leading/trailing/superfluous commas and duplicates."
    return joinTags(sorted(set(parseTags(tags))))

def findTag(tag, tags):
    "True if TAG is in TAGS. Ignore case."
    if not isinstance(tags, types.ListType):
        tags = parseTags(tags)
    return tag.lower() in [t.lower() for t in tags]

def addTags(tagstr, tags):
    "Add tags if they don't exist."
    currentTags = parseTags(tags)
    for tag in parseTags(tagstr):
        if not findTag(tag, currentTags):
            currentTags.append(tag)
    return joinTags(currentTags)

def deleteTags(tagstr, tags):
    "Delete tags if they don't exists."
    currentTags = parseTags(tags)
    for tag in parseTags(tagstr):
        try:
            currentTags.remove(tag)
        except ValueError:
            pass
    return joinTags(currentTags)

# Misc
##############################################################################

def checksum(data):
    return md5(data).hexdigest()
