// @license magnet:?xt=urn:btih:8e4f440f4c65981c5bf93c76d35135ba5064d8b7&dn=apache-2.0.txt Apache-2.0
// (the above comment is for LibreJS)

// Web page typography helper v1.55 (c) 2011-2014,2016,2019-2023 Silas S. Brown.

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Where to find history and documentation:
// on GitHub at https://github.com/ssb22/web-typography
// and on GitLab at https://gitlab.com/ssb22/web-typography
// and on BitBucket https://bitbucket.org/ssb22/web-typography
// and at https://gitlab.developers.cam.ac.uk/ssb22/web-typography
// and in China: https://gitee.com/ssb22/web-typography

var do_punctuation = true, do_spacing = true;
var do_ligatures = (navigator.userAgent.search("Chrome|Safari")>-1 && navigator.userAgent.search("Windows")==-1 && !(typeof(CSS) != 'undefined' && CSS.supports && CSS.supports("font-variant-ligatures", "normal"))); // find-as-you-type in (at least some versions of) Firefox etc doesn't work, and the Windows screenreader JAWS doesn't read them (although NVDA works).  We could disable ligatures if MSAA is in use, but detecting that requires Flash and can take time, plus it doesn't fix find-as-you-type.  But find-as-you-type works just fine in Safari and Chrome, although I haven't been able to test any screenreaders on Mac etc.  So, for now, we enable ligatures if and only if we're on Safari or Chrome on a non-Windows platform and it's too old to do ligatures by itself (e.g. Safari 6.1 on MacOS 10.7.5).

function fix_typography(){} function typefix(s){return s} // no-ops unless we can do:
if(document.getElementsByTagName && navigator.userAgent.indexOf("Googlebot/")==-1) {
  // (Googlebot now executes Javascript, but we don't want
  // it caching the "typography done" versions of pages,
  // otherwise search results might look bad on older
  // computers that can't display the typography, plus some
  // keywords might not be found if ligatures are used. So
  // we ask the bot not to execute this particular script.
  // Hopefully it won't 'punish' a mention of itself by
  // down-ranking the page.)
  
  // (If you have access to the site's /robots.txt then you
  // might also try "Disallow"ing the typography.js URL)

  // (Note: it does NOT seem necessary to stop Googlebot from
  // executing "collapse a paragraph behind a link" code - it
  // seems to know how to expand that JS link and therefore
  // will index the paragraph.  But I'm not so sure about
  // letting it loose on the results of a typography script.)
  
  var b=document.getElementsByTagName("BODY")[0],
      d=document.createElement("DIV"),s=document.createElement("SPAN");
    s.setAttribute("lang","en"); // some systems don't make em-dash wider than en-dash in Chinese etc
  d.appendChild(s);
  var supports_dashes = false, supports_ligatures = false,
    supports_spacing = false, supports_0space = false;
  if (do_punctuation) {
    s.innerHTML = "\u2014";
    b.appendChild(d); var emWidth = s.offsetWidth; b.removeChild(d);
    s.innerHTML = "\u2013";
    b.appendChild(d); var enWidth = s.offsetWidth; b.removeChild(d);
    supports_dashes = emWidth > enWidth; // If they're both the same, they could both be "tofu blocks" on an old system, so play safe and do typography only if we see a difference here
  } if (do_ligatures) {
    s.innerHTML = "\ufb01";
    b.appendChild(d); var fiWidth = s.offsetWidth; b.removeChild(d);
    s.innerHTML = "\ufb03";
    b.appendChild(d); var ffiWidth = s.offsetWidth; b.removeChild(d);
    supports_ligatures = ffiWidth > fiWidth;
  } if (do_spacing) {
    s.innerHTML = "\u2002";
    b.appendChild(d); var enWidth = s.offsetWidth; b.removeChild(d);
    s.innerHTML = "\u2003";
    b.appendChild(d); var emWidth = s.offsetWidth; b.removeChild(d);
    supports_spacing = emWidth > enWidth;
    if (supports_spacing) {
      s.innerHTML = "\u200B";
      b.appendChild(d); var s0Width = s.offsetWidth; b.removeChild(d);
        supports_0space = (s0Width == 0);
    }
  }
  if (supports_dashes || supports_ligatures || supports_spacing) {
  typefix = function(str) {
      if (supports_dashes) str=str.replace(/'neath /g,"\u2019neath ").replace(/ '11 /g," \u201911 ").replace(/'mid /g,"\u2019mid ").replace(/'s /g,"\u2019s ").replace(/---/g,"\u2014").replace(/--/g,"\u2013").replace(/[ \n]'/g," \u2018").replace(/``/g,"\u201C").replace(/`/g,"\u2018").replace(/^''([a-zA-Z])/,"\u201C$1").replace(/^'([a-zA-Z])/,"\u2018$1").replace(/''/g,"\u201D").replace(/'/g,"\u2019").replace(/[ \n]"/g," \u201C").replace(/^"([a-zA-Z])/,"\u201C$1").replace(/\("/g,"(\u201C").replace(/"/g,"\u201D");
    // (ought to be able to say \s instead of [ \n] above, but it doesn't seem to work on all browsers; however we will use it for supports_spacing below as that's less likely to look right on browsers that don't support \s anyway)
    if (supports_spacing) str=str.replace(/([A-Za-z0-9\u2019][A-Za-z0-9][)\u2019\u201d]*(((<[/].*?>)|(<!--.*?-->))[)\u2019\u201d]*)*[.?!][)\u2019\u201d]*(<!--.*?-->)*[)\u2019\u201d]*)\s+((<[^>]*>|<!--.*?-->\s*)*[^A-Za-z0-9]*[A-Z])/g,"$1\u2002"+(supports_0space?"\u200B":"")+"$7"); // use en-space between sentences (must be after quote substitution above), plus zero-width space (if supported) to confirm this is a breakpoint (as some versions of at least Webkit don't break at en-space by default)
    if (supports_ligatures) str=str.replace(/([^f])fi/g,"$1\ufb01").replace(/([^f])fl/g,"$1\ufb02");
    // .replace(/ff/g,"\ufb00"); - doesn't always work so well (might be a different font)
    // also took out .replace(/ffl/g,"\ufb04").replace(/ffi/g,"\ufb03")
    // (TODO how do we check fi and fl use the same font?  should do most of the time)
    return str;
  }
  if(!Array.prototype.includes) Array.prototype.includes=function(v){var i;for(i=0;i < this.length;i++) if(this[i]==v) return true };
  if(typeof(typography_omit)=='undefined') typography_omit=["script","code","pre","tt","kbd","textarea","style","samp","var"];
  function treewalk(c) {
   var d=c.firstChild; while(d) { var n=d.nextSibling; if(d.nodeType==8 && d.previousSibling && d.nextSibling && d.previousSibling.nodeType==3 && d.nextSibling.nodeType==3) c.removeChild(d); else if(d.nodeType==3 && d.previousSibling && d.previousSibling.nodeType==3) { d.previousSibling.nodeValue += d.nodeValue; c.removeChild(d) } d=n; } // remove comments + merge text nodes (so can search/replace across them e.g. for sentence spacing if we had a comment between sentences)
   c=c.firstChild;
   while(c) {
    switch (c.nodeType) {
    case 1: // element
        if (c.nodeName) {
          if(!typography_omit.includes(c.nodeName.toLowerCase())) {
            treewalk(c);
          }
        }
        break;
    case 3: // text
        var v=c.nodeValue;
        var followed = c.nextSibling && c.nextSibling.nodeType==1 && ["span","a","em","strong"].includes(c.nextSibling.nodeName.toLowerCase()) && c.nextSibling.innerHTML.match(/^[^A-Za-z0-9<]*[A-Z]/);
        if (followed) v += "A"; // so can match 'end of sentence. <span>More...'
        var v2=typefix(v);
        if (followed) v2=v2.slice(0,-1); // rm "A"
        if(v2!=v) c.nodeValue=v2;
    }
    c=c.nextSibling;
   }
  }
  fix_typography=function(){treewalk(document)}
  }
} fix_typography();

function hide0(id) {} // no-op unless we can do:
if(document.getElementsByClassName && navigator.userAgent.slice(-6)!='Gecko/') { // 'Gecko/' at the end is presented to JS by UC Browser's transcoder, which lets you set v.OIH but then forgets it by the time show0 is called, so don't do it
    function _h(v) {
        if(location.hash) {
            if(location.hash=="#"+v.id) return; // don't collapse if using id from an off-page link
            var p=v.previousSibling; if(p && p.nodeType==1 && p.nodeName.toLowerCase()=='a' && location.hash=="#"+p.getAttribute("name")) return; // or if using <a name=".."></a> immediately before (for backward compatibility with browsers that can't jump to an id) and we jumped to that
        }
        if(v.innerHTML) { v.OIH=v.innerHTML; if(v.OIH==v.innerHTML) {
            // looks like we have the browser support we need to collapse
            var txt=v.getAttribute("data-txt"),opt=v.getAttribute("data-opt"),c1="",c2="";
            if(opt=="centre") { c1="<center>"; c2="<"+"/center>"; }
            var inline = (opt=="inline" || opt=="inline-ftn");
            if(!txt) txt="Show details";
            v.innerHTML=c1+"<a href=\"#"+v.id+"\" onClick=\"javascript:var v=document.getElementById('"+v.id+"'); v.innerHTML=v.OIH; v.style=v.OS; "+(opt=="inline-ftn"?"window.scrollTo(0,document.body.scrollHeight);v.scrollIntoView();v.parentElement.style='font-size:1em';":"")+"if(v.getElementsByTagName){var abbrs=v.getElementsByTagName('abbr');for(var i=0;i<abbrs.length;i++)abbrs[i].onclick=Function('alert(this.title)')}return false;\">"+typefix(txt)+"<"+"/a>"+c2;
            v.OS=v.style; if(!inline)v.style="display:block!important"
        } }
    } hide0=function(id){_h(document.getElementById(id));}
    var toC=document.getElementsByClassName("collapsed"),i,nID=1;for(i=0;i < toC.length; i++) {
        var v=toC[i];
        if(!v.id) { // make sure it has an ID
            while(document.getElementById(""+nID)) ++nID;
            v.id=""+nID;
        } _h(v);
    }
}

if(document.getElementsByTagName){var abbrs=document.getElementsByTagName('abbr');for(var i=0;i<abbrs.length;i++)abbrs[i].onclick=Function("alert(this.title)")}

// @license-end
