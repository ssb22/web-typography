// Web page typography helper v1.32 (c) 2011-2014,2016,2019-2020 Silas S. Brown.
// @license magnet:?xt=urn:btih:1f739d935676111cfff4b4693e3816e664797050&dn=gpl-3.0.txt GPL-v3-or-Later

// Purpose: Adds typographical characters to your Web pages ONLY IF the
// browser supports them
// (so they'll still work in basic/mobile browsers with ASCII only)

// Usage: At the END of the page (before </body>) do:
// <script src="typography.js"></script>

// The script will also work on OIH attributes (old innerHTML)
// in case you use my method of hiding some verbosity until a "Show" link is activated

// Where to find history:
// on GitHub at https://github.com/ssb22/web-typography
// and on GitLab at https://gitlab.com/ssb22/web-typography
// and on BitBucket https://bitbucket.org/ssb22/web-typography

var do_punctuation = true, do_spacing = true;
// var do_ligatures = false; // Disadvantages of Unicode ligatures even in Web browsers that support them: find-as-you-type in (at least some versions of) Firefox etc doesn't work, and the Windows screenreader JAWS doesn't read them (although NVDA works).  We could disable ligatures if MSAA is in use, but detecting that requires Flash and can take time, plus it doesn't fix find-as-you-type.
// However, find-as-you-type works just fine in Safari and Chrome, although I haven't been able to test any screenreaders on Mac etc.  So, for now, we enable ligatures if and only if we're on Safari or Chrome on a non-Windows platform and it's too old to do ligatures by itself (e.g. Safari 6.1 on MacOS 10.7.5).
var do_ligatures = (navigator.userAgent.search("Chrome|Safari")>-1 && navigator.userAgent.search("Windows")==-1 && !(typeof(CSS) != 'undefined' && CSS.supports && CSS.supports("font-variant-ligatures", "normal")));

function fix_typography() {} // no-op unless we can do:
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
  var supports_dashes = false, supports_ligatures = false, supports_spacing = false;
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
  }
  if (supports_dashes || supports_ligatures || supports_spacing) {
  function typefix(str) {
      if (supports_dashes) str=str.replace(/'neath /g,"\u2019neath ").replace(/'mid /g,"\u2019mid ").replace(/'s /g,"\u2019s ").replace(/---/g,"\u2014").replace(/--/g,"\u2013").replace(/\u2013>/g,"-->").replace(/<!\u2013/g,"<!--").replace(/[ \n]'/g," \u2018").replace(/``/g,"\u201C").replace(/`/g,"\u2018").replace(/^''([a-zA-Z])/,"\u201C$1").replace(/^'([a-zA-Z])/,"\u2018$1").replace(/''/g,"\u201D").replace(/'/g,"\u2019").replace(/[ \n]"/g," \u201C").replace(/^"([a-zA-Z])/,"\u201C$1").replace(/\("/g,"(\u201C").replace(/"/g,"\u201D").replace(/\=\u201D([^\u201D]*)\u201D/g,'="$1"');
    // - comments and = stuff are for OIH markup; may still get problems if OIH contains kbd/samp/var/tt/pre/code with -- or fi etc (in this case try inserting comments in between the hyphens), ligatures (ditto), or quotes (and can't work around by using &quot; - try adding 'undo' exceptions to the end, or make sure the 'hide' code goes AFTER the inclusion of typography.js)
    // (ought to be able to say \s instead of [ \n], but it doesn't seem to work on all browsers)
    if (supports_spacing) str=str.replace(/([A-Za-z][A-Za-z][.?!])\s+([^A-Za-z]*[A-Z])/g,"$1\u2002$2"); // use en-space between sentences (TODO: check for HTML comments between sentences?  close-quotes before the space?)
    if (supports_ligatures) str=str.replace(/([^f])fi/g,"$1\ufb01").replace(/([^f])fl/g,"$1\ufb02");
    // .replace(/ff/g,"\ufb00"); - doesn't always work so well (might be a different font)
    // also took out .replace(/ffl/g,"\ufb04").replace(/ffi/g,"\ufb03")
    // (TODO how do we check fi and fl use the same font?  should do most of the time)
    return str;
  }
  if(!Array.prototype.includes) Array.prototype.includes=function(v){var i;for(i=0;i < this.length;i++) if(this[i]==v) return true };
  if(typeof(typography_omit)=='undefined') typography_omit=["script","code","pre","tt","kbd","textarea","style","samp","var"];
  function treewalk(c) {
   c=c.firstChild;
   while(c) {
    switch (c.nodeType) {
    case 1: // element
        if (c.nodeName) {
          if(!typography_omit.includes(c.nodeName.toLowerCase())) {
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
  fix_typography=function(){treewalk(document)}
  }
} fix_typography();

// oh, and provide onclick for abbr tags:
if(document.getElementsByTagName){var abbrs=document.getElementsByTagName('abbr');for(var i=0;i<abbrs.length;i++)abbrs[i].onclick=Function("alert(this.title)")}

// @license-end
