#!/usr/bin/env python
# (should work on both Python 2 and Python 3)

"""Convert simple HTML pages into Gemini pages with some typography
Version 1.57 (c) 2021-25 Silas S. Brown.  License: Apache 2"""

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

# Example output: most of the pages on
# gemini://gemini.ctrl-c.club/~ssb22/
# and gemini://tilde.pink/~ssb22/

import re, sys, os
if sys.stdin.isatty():
    print (__doc__+"\n\nUse python html2gmi.py < inputfile or use in a pipe\nAlso has a --markdown switch for generating simple md instead of gmi")
    sys.exit()
markdown_mode = "--markdown" in sys.argv
d = sys.stdin.read()
is_python2 = not type(d)==type(u"")
if is_python2: d=d.decode('utf-8')
try: from urlparse import urljoin
except: from urllib.parse import urljoin

assert not "<if " in d.lower() # we can't do htp macro processing

# Remove comments and HEAD
# (this assumes scripts are in comments, no <style> in body, etc)
d = re.sub("(?s)<!--.*?-->","",
           re.sub("(?si).*<body","<body",d))

# Remove extra newlines and whitespace, except in <pre>
assert not "%@space@%" in d
assert not "%@sharp@%" in d
d = d.replace("#","%@sharp@%") # don't confuse comments with Gemini headings
d = re.sub("(?si)<pre[^a-z].*?</pre>",lambda m:re.sub("<pre[^>]+>","<pre>",m.group()).replace("\n","<br>"+("%@space@%" if markdown_mode else "")).replace(" ","%@space@%"),d)
d = ' '.join(d.split())

# Ensure line-breaks in blockquote stay in blockquote
d = re.sub("(?i)<blockquote[^a-z].*?</blockquote>",lambda m:re.sub("(?i)<(/?)(p|br)([^a-z>][^>]*)?>",r"<\1blockquote>",m.group()),d)

# Protect quotes, hyphens etc in <code> <kbd> etc
assert not "%@quot" in d
to_protect = '"'+"'-?!.`"
def protect(s):
    try: s = s.group()
    except: pass # not a regex match
    s = s.replace('&quot;','"') # needed or &quot; quotes in <kbd> won't be protected from the rewrite
    if markdown_mode and s.startswith("<") and not s.lower().startswith("<pre"): s="`"+s+"`" # pre already has ``` added below
    for i,c in enumerate(to_protect):
        s = s.replace(c,"%@quot"+str(i))
    return s
def unprotect(s):
    for i,c in enumerate(to_protect):
        s = s.replace("%@quot"+str(i),c)
    return s.replace("%@quotS"," ")
d = re.sub("(?i)<(kbd|code|tt|pre|samp|var)([^a-z>][^>]*)?>.*?</(kbd|code|tt|pre|samp|var)([^a-z>][^>]*)?>",protect,d) # (pre will be all on one line with <br> by this time)

# Apply simple Gemini formatting for some tags
d = re.sub("(?i)<(p|div|details|summary)([^a-z>][^>]*)?>","\n",d)
sharps = "#"
for n in range(1,7):
    if "<h"+str(n) in d.lower():
        d = re.sub("<[hH]"+str(n)+"[^>]*>","\n"+sharps+" ",d)
        if len(sharps) < 3: sharps += "#"
d = re.sub("</[hH][^>]*>","\n",d)
n_stack = []
def number(m):
    m = m.group()
    if "<li" in m.lower():
        if markdown_mode: r="%@quotS%@quotS"*(len(n_stack)-1)+(str(n_stack[-1])+'.' if n_stack[-1] else "*")
        else:
            r = ''.join(str(i)+'.' for i in n_stack if i)
            if not r: r = "*"
        if n_stack[-1]: n_stack[-1] += 1
        return "<br>"+r+" "
    elif "<ul" in m.lower(): n_stack.append(0)
    elif "<ol" in m.lower(): n_stack.append(1)
    elif "</ul" in m.lower() or "</ol" in m.lower(): n_stack.pop()
    return m
d = re.sub("(?i)</?([uo]l|li)([^>a-z][^>]*)?>",number,d)
d = re.sub("(?i)<br([^a-z>][^>]*)?>","\n",d)
d = re.sub("(?i)<dt([^a-z>][^>]*)?>","\n* ",d)
d = re.sub("(?i)<dd([^a-z>][^>]*)?>",":<dd> ",d).replace("::<dd>",":").replace(":<dd>",":") # dt-dd transition (but don't add second : if already one there)
d = re.sub("(?i)<blockquote([^a-z>][^>]*)?>","\n> ",d)
d = re.sub("(?i)</?pre([^a-z>][^>]*)?>","\n"+protect("```")+"\n",d)
d = re.sub("(?i)</(blockquote|dl|ol|ul|div|details|summary)([^a-z>][^>]*)?>","\n",d)
d = re.sub("(?i)<hr([^a-z>][^>]*)?>","\n",d)
# and simple tables:
d = re.sub("(?i)<tr([^a-z>][^>]*)?><th([^a-z>][^>]*)?>","\n### ",d)
d = re.sub("(?mi)^### (.*<td)",r"\1",d) # (this assumes 1 row = 1 line of HTML: removes subheading tag if not all row is headings, e.g. if only leftmost cell is heading)
d = re.sub("(?i)</?tr([^a-z>][^>]*)?>","\n",d)
d = re.sub("(?i)</t[hd]><t[hd]([^a-z>][^>]*)?>"," - ",d) # or "---" for em-dash, but spaced hyphen might be better as it's not quite the same as running text (could try " -- " for spaced en-dash)
d = re.sub("(?i)[)]</rb><rt([^a-z>][^>]*)?>(.*?)</rt>",r" \2)",d) # ruby w. close-paren around rb: relocate to end of rt + add space
d = re.sub("(?i)<rt([^a-z>][^>]*)?>",r" ",d)

# Non-standard * for emphasis (OK for <em>, probably not for <strong> that might be used to emphasize longer statements)
d = re.sub("(?i)</*em[^>]*>","*",d)
if markdown_mode: d = re.sub("(?i)</*strong[^>]*>","**",re.sub("(?i)</*b[^a-z>]*>","**",d))

if "base_href" in os.environ:
    d = d.split("\n");i=0
    while i<len(d):
        for m in re.finditer("(?i)<a [^>]*href=(\"[^\"]*\"|[^ >]*)( [^>]*)?>(.*?)</a>",d[i]):
            newURL = urljoin(os.environ["base_href"],m.group(1).replace('"',''))
            lastBit = newURL.split("/")[-1]
            if "link_nonhtml_only" in os.environ and (not '.' in lastBit or '.htm' in lastBit or '#' in lastBit): pass # skip a link that looks like it goes to HTML rather than to a downloadable file
            else:
                linkTxt = m.groups()[-1]
                if linkTxt=="this" and lastBit: linkTxt = lastBit
                if re.sub("<[^>]*>","",linkTxt).split()==re.sub("<[^>]*>","",d[i]).split(): del d[i] # entire line is the link, so just replace it
                else: i+=1
                d.insert(i,"=> "+newURL.replace("https://github.com","https://www.github.com",1)+" "+linkTxt) # .replace() to work around a bug in deedum 2022.0406 for Android: if GitHub's own app is also installed on the same device, deedum says "Cannot find app to handle https://github.com", but with www is OK
        i += 1
    d = "\n".join(d)
if "images" in os.environ: # set to list of allowed images.  Some Gemini clients can show images inline if and only if they're served over Gemini, but others can show only if they're HTTP, so we provide both if base_href is set as well.
    # as of end-2021: Ariane (and its commercial replacement?) shows Gemini images inline; Lagrange can click to show Gemini images inline; Deedum shows Gemini images in same app; Xenia shows just a box unless the images are http
    d = d.split("\n");i=0
    while i<len(d):
        for m in re.finditer("(?i)<img [^>]*src=(\"[^\"]*\"|[^ >]*)( [^>]*)?>",d[i]):
            src = m.group(1).replace('"','')
            if src in os.environ["images"].split():
                i+=1;d.insert(i,"=> "+src+" "+src) # TODO: or alt, if non-empty
                if "base_href" in os.environ:
                    i+=1;d.insert(i,"=> "+urljoin(os.environ["base_href"],src)+" "+src+" over HTTP")
        i += 1
    d = "\n".join(d)

# Remove other tags + handle HTML entities
d = re.sub('<([^>"]*|("[^"]*"))+>',"",d)
try: import htmlentitydefs
except: import html.entities as htmlentitydefs
try: unichr # Python 2
except: unichr = chr # Python 3
d = re.sub("[&]([a-zA-Z0-9]+);",lambda m:unichr(0)+unichr(htmlentitydefs.name2codepoint.get(m.group(1),63))+unichr(0),d)
d = re.sub("[&]%@sharp@%x([0-9A-Fa-f]+);",lambda m:unichr(0)+unichr(int(m.group(1),16))+unichr(0),d)
d = re.sub("[&]%@sharp@%([0-9]+);",lambda m:unichr(int(m.group(1))),d).replace(unichr(0),u"")
d = d.replace(unichr(0xAD),u"") # soft hyphen (meant to be an optional hyphenation point, e.g. for giant-print display, but some clients e.g. Elpher in Emacs might always display)

# Apply typography.js rules
d = d.replace("'neath ",u"\u2019neath ").replace(" '11 ",u" \u201911 ").replace("'mid ",u"\u2019mid ").replace("'s ",u"\u2019s ").replace("---",u"\u2014").replace("--",u"\u2013").replace(" '",u" \u2018").replace("``",u"\u201C").replace("`",u"\u2018")
d = re.sub("(?mi)^''(?=[a-z])",u"\u201c",d)
d = re.sub("(?mi)^'(?=[a-z])",u"\u2018",d)
d = d.replace("''",u"\u201D").replace("'",u"\u2019").replace(' "',u" \u201C")
d = re.sub('(?mi)^"(?=[a-z])',u"\u201C",d).replace('("',u"(\u201C").replace('"',u"\u201D")
d = re.sub(u"([A-Za-z0-9\u2019][A-Za-z0-9][)\u2019\u201d]*[.?!][)\u2019\u201d]*) +(?=[^A-Za-z0-9]*[A-Z])",u"\\1  " if markdown_mode else u"\\1\u2002",d) # spacing

# clean up, and restore <pre> formatting
d = re.sub("^\s+","",re.sub("\s*\n\s*","\n",re.sub('  +',' ',d)))
if markdown_mode: d=re.sub("\n(?!((%@quotS)*(\\*|[1-9][0-9]*[.]) )|(%@space@%)|("+protect("```")+"))","\n\n",d).replace(protect("```")+"\n\n",protect("```")+"\n")
d = d.replace("\n%@sharp@%",u"\n\u200B#").replace("%@sharp@%","#")
d = unprotect(d.replace("%@space@%"," "))

if is_python2: d=d.encode('utf-8')
sys.stdout.write(d)
