#!/usr/bin/env python

# Convert simple HTML pages into Gemini pages with some typography
# Version 1.48 (c) 2021-23 Silas S. Brown

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

import re, sys, os
d = sys.stdin.read()
is_python2 = not type(d)==type(u"")
if is_python2: d=d.decode('utf-8')
try: from urlparse import urljoin
except: from urllib.parse import urljoin

assert not "<if " in d.lower() # we can't do htp macro processing

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
    s = s.replace('&quot;','"') # needed or &quot; quotes in <kbd> won't be protected from the rewrite
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
# and simple tables:
d = re.sub("<[tT][rR]([^A-Za-z>][^>]*)?><[tT][hH]([^A-Za-z>][^>]*)?>","\n### ",d)
d = re.sub("^### (.*<[tT][dD])",r"\1",d,flags=re.MULTILINE) # (this assumes 1 row = 1 line of HTML: removes subheading tag if not all row is headings, e.g. if only leftmost cell is heading)
d = re.sub("</?[tT][rR]([^A-Za-z>][^>]*)?>","\n",d)
d = re.sub("</[tT][hHdD]><[tT][hHdD]([^A-Za-z>][^>]*)?>"," - ",d) # or "---" for em-dash, but spaced hyphen might be better as it's not quite the same as running text (could try " -- " for spaced en-dash)
d = re.sub("[)]</[rR][bB]><[rR][tT]([^A-Za-z>][^>]*)?>(.*?)</[rR][tT]>",r" \2)",d) # ruby w. close-paren around rb: relocate to end of rt + add space
d = re.sub("<[rR][tT]([^A-Za-z>][^>]*)?>",r" ",d)

# Non-standard * for emphasis (OK for <em>, probably not for <strong> that might be used to emphasize longer statements)
d = re.sub("</*[eE][mM][^>]*>","*",d)

if "base_href" in os.environ:
    d = d.split("\n");i=0
    while i<len(d):
        for m in re.finditer("<a [^>]*href=(\"[^\"]*\"|[^ >]*)( [^>]*)?>(.*?)</a>",d[i],re.I):
            newURL = urljoin(os.environ["base_href"],m.group(1).replace('"',''))
            lastBit = newURL.split("/")[-1]
            if "link_nonhtml_only" in os.environ and (not '.' in lastBit or '.htm' in lastBit or '#' in lastBit): pass # skip a link that looks like it goes to HTML rather than to a downloadable file
            else:
                linkTxt = m.groups()[-1]
                if linkTxt=="this" and lastBit: linkTxt = lastBit
                if re.sub("<[^>]*>","",linkTxt).split()==re.sub("<[^>]*>","",d[i]).split(): del d[i] # entire line is the link, so just replace it
                else: i+=1
                d.insert(i,"=> "+newURL+" "+linkTxt)
        i += 1
    d = "\n".join(d)
if "images" in os.environ: # set to list of allowed images.  Some Gemini clients can show images inline if and only if they're served over Gemini, but others can show only if they're HTTP, so we provide both if base_href is set as well.
    # as of end-2021: Ariane (and its commercial replacement?) shows Gemini images inline; Lagrange can click to show Gemini images inline; Deedum shows Gemini images in same app; Xenia shows just a box unless the images are http
    d = d.split("\n");i=0
    while i<len(d):
        for m in re.finditer("<img [^>]*src=(\"[^\"]*\"|[^ >]*)( [^>]*)?>",d[i],re.I):
            src = m.group(1).replace('"','')
            if src in os.environ["images"].split():
                i+=1;d.insert(i,"=> "+src+" "+src) # TODO: or alt, if non-empty
                if "base_href" in os.environ:
                    i+=1;d.insert(i,"=> "+urljoin(os.environ["base_href"],src)+" "+src+" over HTTP")
        i += 1
    d = "\n".join(d)

# Remove other tags + handle HTML entities
d = re.sub("<[^>]*>","",d)
try: import htmlentitydefs
except: import html.entities as htmlentitydefs
try: unichr # Python 2
except: unichr = chr # Python 3
d = re.sub("[&][a-zA-Z0-9]+;",lambda m:unichr(htmlentitydefs.name2codepoint.get(m.group()[1:-1],63)),d)

# Apply typography.js rules
d = d.replace("'neath ",u"\u2019neath ").replace(" '11 ",u" \u201911 ").replace("'mid ",u"\u2019mid ").replace("'s ",u"\u2019s ").replace("---",u"\u2014").replace("--",u"\u2013").replace(" '",u" \u2018").replace("``",u"\u201C").replace("`",u"\u2018")
d = re.sub("^''(?=[a-zA-Z])",u"\u201c",d,flags=re.M)
d = re.sub("^'(?=[a-zA-Z])",u"\u2018",d,flags=re.M)
d = d.replace("''",u"\u201D").replace("'",u"\u2019").replace(' "',u" \u201C")
d = re.sub('^"(?=[a-zA-Z])',u"\u201C",d,flags=re.M).replace('("',u"(\u201C").replace('"',u"\u201D")
d = re.sub(u"([A-Za-z0-9\u2019][A-Za-z0-9][)\u2019\u201d]*[.?!][)\u2019\u201d]*) +(?=[^A-Za-z0-9]*[A-Z])",u"\\1\u2002",d) # spacing

# clean up, and restore <pre> formatting
d = re.sub("^\s+","",re.sub("\s*\n\s*","\n",re.sub('  +',' ',d)))
d = unprotect(d.replace("%@space@%"," "))

if is_python2: d=d.encode('utf-8')
sys.stdout.write(d)
