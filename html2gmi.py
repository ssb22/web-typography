#!/usr/bin/env python

# Convert simple HTML pages into Gemini pages with some typography
# (c) 2021 Silas S. Brown

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Where to find history:
# on GitHub at https://github.com/ssb22/web-typography
# and on GitLab at https://gitlab.com/ssb22/web-typography
# and on BitBucket https://bitbucket.org/ssb22/web-typography
# and at https://gitlab.developers.cam.ac.uk/ssb22/web-typography
# and in China: https://gitee.com/ssb22/web-typography

import re, sys
d = sys.stdin.read()
is_python2 = not type(d)==type(u"")
if is_python2: d=d.decode('utf-8')

# Remove extra newlines and whitespace
assert not "<pre" in d.lower(), "pre not yet implemented" # TODO: use >
d = ' '.join(d.split())

# Remove comments and HEAD
# (this assumes scripts are in comments, no <style> in body, etc)
d = re.sub("<!--.*?-->","",d)
d = re.sub(".*<[bB][oO][dD][yY]","<body",d)

# Apply simple Gemini formatting for some tags
d = re.sub("<[pP][^>]*>","\n",d)
d = re.sub("<[hH][^>]*>","\n# ",d) # TODO: heading levels
d = re.sub("<[bB][rR][^>]*>","\n",d)
d = re.sub("<[lL][iI][^>]*>","\n* ",d)
d = re.sub("<[dD][tT][^>]*>","\n* ",d)
d = re.sub("</[dDoOuU][lL][^>]*>","\n",d)
d = re.sub("</[hH][^>]*>","\n",d)

# Non-standard * for emphasis (ok for em, probably not for strong that might be used to emphasize longer statements)
d = re.sub("</*[eE][mM][^>]*>","*",d)

# Remove other tags + handle HTML entities
d = re.sub("<[^>]*>","",d)
d = d.replace("&nbsp;"," ").replace("&amp;","&").replace("&lt;","<")
assert not re.search("&[^ ;*];",d), "unhandled entity"

# Apply typography.js rules
# (TODO: omit pre from this if supporting)
d = d.replace("'neath ",u"\u2019neath ").replace(" '11 ",u" \u201911 ").replace("'mid ",u"\u2019mid ").replace("'s ",u"\u2019s ").replace("---",u"\u2014").replace("--",u"\u2013").replace(" '",u" \u2018").replace("``",u"\u201C").replace("`",u"\u2018")
d = re.sub("^''(?=[a-zA-Z])",u"\u201c",d,flags=re.M)
d = re.sub("^'(?=[a-zA-Z])",u"\u2018",d,flags=re.M)
d = d.replace("''",u"\u201D").replace("'",u"\u2019").replace(' "',u" \u201C")
d = re.sub('^"(?=[a-zA-Z])',u"\u201C",d,flags=re.M).replace('("',u"(\u201C").replace('"',u"\u201D")
d = re.sub(ur"([A-Za-z][A-Za-z][)]?([)]?)*[.?!][)\u2019\u201d]*[)\u2019\u201d]*) +(?=[^A-Za-z]*[A-Z])",u"\\1\u2002",d) # spacing
d = re.sub("^\s+","",re.sub("\s*\n\s*","\n",d))

if is_python2: d=d.encode('utf-8')
sys.stdout.write(d)
