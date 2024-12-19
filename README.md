# web-typography

I like to have "nice typography" on my website:

* Punctuation (curved quotes and em-dashes)
* En-space between sentences
* Ligatures

but I also want:

* "Graceful degradation" in old browsers that can't display the Unicode
  (so at least my English pages should be fully readable in ASCII-only)

* All screen readers and search functions to work
  without being 'tripped up' by ligatures

Therefore I generally write English text in ASCII, and use this Javascript code
to assess the level of browser support before making substitutions.
If Javascript is not available then my site should still be readable in ASCII.

While the main point of this script is typography, it also provides
an `onclick` function for every `abbr` tag (helps in touchscreen situations
with no mouse if you're using `<abbr title="...">`).
Again if Javascript is not available then this is simply not done; the page
should still be readable.

Usage
-----

At the **end** of each page (before `</body>`), put
`<script src="typography.js"></script>`
(or arrange for this to be added into the site's template if you have one).
**Please mirror the script locally to avoid depending on my servers.**

If your own Javascript _later_ adds new text to the page as a result of a user
interaction, you might then want to call `fix_typography()` after doing so, but
in most cases this should not be necessary. (You may optionally override the
`typography_omit` array before including the script and/or before calling
`fix_typography()`, if you want to set a different set of elements inside which
nice typography is not to be attempted, but be careful if overriding this.)

Trademarks
----------

Javascript is a trademark of Oracle Corporation in the US.
Unicode is a registered trademark of Unicode, Inc. in the United States and other countries.
Any other trademarks I mentioned without realising are trademarks of their respective holders.
