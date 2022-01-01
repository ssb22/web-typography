#!/usr/bin/env python

# Convert simple HTML pages into Gemini pages with some typography
# Version 1.2 (c) 2021 Silas S. Brown

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

# Remove comments and HEAD
# (this assumes scripts are in comments, no <style> in body, etc)
d = re.sub("<!--.*?-->","",d,flags=re.DOTALL)
d = re.sub(".*<[bB][oO][dD][yY]","<body",d,flags=re.DOTALL)

# Remove extra newlines and whitespace, except in <pre>
assert not "%@space@%" in d
d = re.sub("<pre[^a-z].*?</pre>",lambda m:re.sub("<pre[^>]+>","<pre>",m.group()).replace("\n","<br>").replace(" ","%@space@%"),d,flags=re.I+re.DOTALL)
d = ' '.join(d.split())

# Ensure line-breaks in blockquote stay in blockquote
d = re.sub("<blockquote[^a-z].*?</blockquote>",lambda m:re.sub("<(/?)(p|br)([^a-z>][^>]*)?>",r"<\1blockquote>",m.group(),flags=re.I),d,flags=re.I)

# Protect quotes, hyphens etc in <code> <kbd> etc
assert not "%@quot" in d
to_protect = '"'+"'-?!.`"
def protect(s):
    try: s = s.group()
    except: pass # not a regex match
    for i,c in enumerate(to_protect):
        s = s.replace(c,"%@quot"+str(i))
    return s
def unprotect(s):
    for i,c in enumerate(to_protect):
        s = s.replace("%@quot"+str(i),c)
    return s
d = re.sub("<(kbd|code|tt|pre|samp|var)([^a-z>][^>]*)?>.*?</(kbd|code|tt|pre|samp|var)([^a-z>][^>]*)?>",protect,d,flags=re.I)

# Apply simple Gemini formatting for some tags
d = re.sub("<[pP]([^A-Za-z>][^>]*)?>","\n",d)
sharps = "#"
for n in range(1,7):
    if "<h"+str(n) in d.lower():
        d = re.sub("<[hH]"+str(n)+"[^>]*>","\n"+sharps+" ",d)
        if len(sharps) < 3: sharps += "#"
d = re.sub("</[hH][^>]*>","\n",d)
n_stack = []
def number(m):
    m = m.group()
    if "<li" in m.lower() and n_stack[-1]:
        n_stack[-1] += 1
        r = "<br>"+'.'.join(str(i-1) for i in n_stack if i)+'. '
        return r
    elif "<ul" in m.lower(): n_stack.append(0)
    elif "<ol" in m.lower(): n_stack.append(1)
    elif "</ul" in m.lower() or "</ol" in m.lower(): n_stack.pop()
    return m
d = re.sub("</?([uo]l|li)([^>A-Za-z][^>]*)?>",number,d,flags=re.I)
d = re.sub("<[bB][rR]([^A-Za-z>][^>]*)?>","\n",d)
d = re.sub("<[lL][iI]([^A-Za-z>][^>]*)?>","\n* ",d) # TODO: 'ol' should be numbered instead (but beware if ul nested inside ol, etc)
d = re.sub("<[dD][tT]([^A-Za-z>][^>]*)?>","\n* ",d)
d = re.sub("<[dD][dD]([^A-Za-z>][^>]*)?>"," ",d) # dt-dd use space
d = re.sub("<blockquote([^A-Za-z>][^>]*)?>","\n> ",d,flags=re.I)
d = re.sub("</blockquote([^A-Za-z>][^>]*)?>","\n",d,flags=re.I)
d = re.sub("</?[pP][rR][eE]([^A-Za-z>][^>]*)?>","\n"+protect("```")+"\n",d)
d = re.sub("</[dDoOuU][lL]([^A-Za-z>][^>]*)?>","\n",d)
d = re.sub("</?[dD][iI][vV]([^A-Za-z>][^>]*)?>","\n",d)
d = re.sub("<[hH][rR]([^A-Za-z>][^>]*)?>","\n",d)

# Non-standard * for emphasis (OK for <em>, probably not for <strong> that might be used to emphasize longer statements)
d = re.sub("</*[eE][mM][^>]*>","*",d)

# Remove other tags + handle HTML entities
d = re.sub("<[^>]*>","",d)
try: import htmlentitydefs
except: import html.entities as htmlentitydefs
try: unichr # Python 2
except: unichr = chr # Pythno 3
d = re.sub("[&][a-zA-Z0-9]+;",lambda m:unichr(htmlentitydefs.name2codepoint.get(m.group()[1:-1],63)),d)

# Apply typography.js rules
d = d.replace("'neath ",u"\u2019neath ").replace(" '11 ",u" \u201911 ").replace("'mid ",u"\u2019mid ").replace("'s ",u"\u2019s ").replace("---",u"\u2014").replace("--",u"\u2013").replace(" '",u" \u2018").replace("``",u"\u201C").replace("`",u"\u2018")
d = re.sub("^''(?=[a-zA-Z])",u"\u201c",d,flags=re.M)
d = re.sub("^'(?=[a-zA-Z])",u"\u2018",d,flags=re.M)
d = d.replace("''",u"\u201D").replace("'",u"\u2019").replace(' "',u" \u201C")
d = re.sub('^"(?=[a-zA-Z])',u"\u201C",d,flags=re.M).replace('("',u"(\u201C").replace('"',u"\u201D")
d = re.sub(ur"([A-Za-z][A-Za-z][)]?([)]?)*[.?!][)\u2019\u201d]*[)\u2019\u201d]*) +(?=[^A-Za-z0-9]*[A-Z])",u"\\1\u2002",d) # spacing

# clean up, and restore <pre> formatting
d = re.sub("^\s+","",re.sub("\s*\n\s*","\n",re.sub('  +',' ',d)))
d = unprotect(d.replace("%@space@%"," "))

if is_python2: d=d.encode('utf-8')
sys.stdout.write(d)
