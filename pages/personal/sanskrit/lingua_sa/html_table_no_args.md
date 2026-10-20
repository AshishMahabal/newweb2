---
title: "html_table_no_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>html_table_no_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(sandhi vibhakti transliterate);</p>

<p>print &ldquo;\nTable of all vibhakti/vachana combination for given noun/linga &ldquo;;
print &ldquo;in UNICODE-devanAgarI as an HTML table\n\n&rdquo;;</p>

<p>my $noun=&ldquo;raama&rdquo;;   # a-kaarant
my $linga = 1;      # alias for &ldquo;puM&rdquo;;</p>

<p>print &ldquo;Using noun $noun, linga $linga\n\n&rdquo;;</p>

<p>print &ldquo;&lt;TABLE BORDER=1&gt;\n&rdquo;;
for my $i (1..8){   # prathamA through sambodhana
    print &ldquo;&lt;TR&gt;&rdquo;;
    for my $j (1..3){   # eka-, dvi-, bahuvachana
        printf &ldquo;&lt;TD&gt;%s&lt;/TD&gt;&rdquo;,
        transliterate(sandhi(vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$i,vachana=&gt;$j})));
        }
     print &ldquo;&lt;/TR&gt;\n&rdquo;;
     }
print &ldquo;&lt;/TABLE&gt;\n&rdquo;;
</CODE></PRE><P>
USAGE: html_table_no_args.pl <P>
OUTPUT<BR>
<PRE></p>

<p>Table of all vibhakti/vachana combination for given noun/linga in UNICODE-devanAgarI as an HTML table</p>

<p>Using noun raama, linga 1</p>

<p><TABLE BORDER=1>
<TR><TD>&#2352;&#2366;&#2350;&#2307; </TD><TD>&#2352;&#2366;&#2350;&#2380; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2307; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2350;&#2381; </TD><TD>&#2352;&#2366;&#2350;&#2380; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2344;&#2381; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2375;&#2339; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2349;&#2381;&#2351;&#2366;&#2350;&#2381; </TD><TD>&#2352;&#2366;&#2350;&#2376;&#2307; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2366;&#2351; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2349;&#2381;&#2351;&#2366;&#2350;&#2381; </TD><TD>&#2352;&#2366;&#2350;&#2375;&#2349;&#2381;&#2351;&#2307; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2366;&#2340;&#2381; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2349;&#2381;&#2351;&#2366;&#2350;&#2381; </TD><TD>&#2352;&#2366;&#2350;&#2375;&#2349;&#2381;&#2351;&#2307; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2360;&#2381;&#2351; </TD><TD>&#2352;&#2366;&#2350;&#2351;&#2379;&#2307; </TD><TD>&#2352;&#2366;&#2350;&#2366;&#2339;&#2366;&#2350;&#2381; </TD></TR>
<TR><TD>&#2352;&#2366;&#2350;&#2375; </TD><TD>&#2352;&#2366;&#2350;&#2351;&#2379;&#2307; </TD><TD>&#2352;&#2366;&#2350;&#2375;&#2359;&#2369; </TD></TR>
<TR><TD>&#2361;&#2375; &#2352;&#2366;&#2350; </TD><TD>&#2361;&#2375; &#2352;&#2366;&#2350;&#2380; </TD><TD>&#2361;&#2375; &#2352;&#2366;&#2350;&#2366;&#2307; </TD></TR>
</TABLE>
</PRE>
</BODY></HTML></p>
</div>
```
