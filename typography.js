// Web page typography helper v1.26 (c) 2011-2014,2016 Silas S. Brown.
// @license magnet:?xt=urn:btih:1f739d935676111cfff4b4693e3816e664797050&dn=gpl-3.0.txt GPL-v3-or-Later

// Purpose: Adds typographical characters to your Web pages ONLY IF the
// browser supports them
// (so they'll still work in basic/mobile browsers with ASCII only)

// Usage: At the END of the page (before </body>) do:
// <script src="typography.js"></script>

// The script will also work on OIH attributes (old innerHTML)
// in case you use my method of hiding some verbosity until a "Show" link is activated

var do_punctuation = true;
// var do_ligatures = false; // Disadvantages of Unicode ligatures even in Web browsers that support them: find-as-you-type in (at least some versions of) Firefox etc doesn't work, and the Windows screenreader JAWS doesn't read them (although NVDA works).  We could disable ligatures if MSAA is in use, but detecting that requires Flash and can take time, plus it doesn't fix find-as-you-type.
// However, find-as-you-type works just fine in Safari and Chrome, although I haven't been able to test any screenreaders on Mac etc:
var do_ligatures = (navigator.userAgent.search("Chrome|Safari")>-1 && navigator.userAgent.search("Windows")==-1);

if(document.getElementsByTagName && navigator.userAgent.indexOf("Googlebot/")==-1) {
  // (Googlebot now executes Javascript, but we don't want
  // it caching the "typography done" versions of pages,
  // otherwise search results might look bad on older
  // computers that can't display the typography, plus some
  // keywords might not be found if ligatures are used. So
  // we ask the bot not to execute this particular script.
  // I only hope it won't 'punish' a mention of itself by
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
  d.appendChild(s);
  var supports_dashes = false, supports_ligatures = false;
  if (do_punctuation) {
    s.innerHTML = "\u2014";
    b.appendChild(d); var emWidth = s.offsetWidth; b.removeChild(d);
    s.innerHTML = "\u2013";
    b.appendChild(d); var enWidth = s.offsetWidth; b.removeChild(d);
    supports_dashes = emWidth > enWidth;
  } if (do_ligatures) {
    s.innerHTML = "\ufb01";
    b.appendChild(d); var fiWidth = s.offsetWidth; b.removeChild(d);
    s.innerHTML = "\ufb03";
    b.appendChild(d); var ffiWidth = s.offsetWidth; b.removeChild(d);
    supports_ligatures = ffiWidth > fiWidth;
  }
  if (supports_dashes || supports_ligatures) {
  function typefix(str) {
      if (supports_dashes) str=str.replace(/'neath /g,"\u2019neath ").replace(/'s /g,"\u2019s ").replace(/---/g,"\u2014").replace(/--/g,"\u2013").replace(/\u2013>/g,"-->").replace(/<!\u2013/g,"<!--").replace(/[ \n]'/g," \u2018").replace(/``/g,"\u201C").replace(/`/g,"\u2018").replace(/^''([a-zA-Z])/,"\u201C$1").replace(/^'([a-zA-Z])/,"\u2018$1").replace(/''/g,"\u201D").replace(/'/g,"\u2019").replace(/[ \n]"/g," \u201C").replace(/^"([a-zA-Z])/,"\u201C$1").replace(/\("/g,"(\u201C").replace(/"/g,"\u201D").replace(/\=\u201D([^\u201D]*)\u201D/g,'="$1"');
    // - comments and = stuff are for OIH markup; may still get problems if OIH contains <tt> or <pre> with -- (in this case try inserting comments in between the hyphens), ligatures (ditto), or quotes (and can't work around by using &quot; - try adding 'undo' exceptions to the end, or make sure the 'hide' code goes AFTER the inclusion of typography.js)
    // (ought to be able to say \s instead of [ \n], but it doesn't seem to work on all browsers)
    if (supports_ligatures) str=str.replace(/fi/g,"\ufb01").replace(/fl/g,"\ufb02");
    // .replace(/ff/g,"\ufb00"); - doesn't always work so well (might be a different font)
    // also took out .replace(/ffl/g,"\ufb04") before fl, and .replace(/ffi/g,"\ufb03") before fi
    // (TODO how do we check fi and fl use the same font?  should do most of the time)
    return str;
  }
  function treewalk(c) {
   c=c.firstChild;
   while(c) {
    switch (c.nodeType) {
    case 1: // element
        if (c.nodeName) {
          var cc = c.nodeName.toLowerCase();
          if (cc!="script" && cc!="code" && cc!="pre" && cc!="tt" && cc!="kbd" && cc!="textarea" && cc!="style" && cc!="samp" && cc!="var") {
            treewalk(c);
            if (c.OIH) c.OIH=typefix(c.OIH);
          }
        }
        break;
    case 3: // text
        c.nodeValue=typefix(c.nodeValue);
    }
    c=c.nextSibling;
   }
  }
  treewalk(document);
  }
}

// oh, and provide onclick for abbr tags:
if(document.getElementsByTagName){var abbrs=document.getElementsByTagName('abbr');for(var i=0;i<abbrs.length;i++)abbrs[i].onclick=Function("alert(this.title)")}

// @license-end
