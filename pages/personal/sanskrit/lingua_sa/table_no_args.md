---
title: "table_no_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>table_no_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(sandhi vibhakti);</p>

<p>print &ldquo;\nTable of all vibhakti/vachana combination for given noun/linga\n\n&rdquo;;</p>

<p>my $noun=&ldquo;raama&rdquo;;   # a-kaarant
my $linga = 1;      # alias for &ldquo;puM&rdquo;;</p>

<p>print &ldquo;Using noun $noun, linga $linga\n\n&rdquo;;</p>

<p>for my $i (1..8){   # prathamA through sambodhana
    for my $j (1..3){   # eka-, dvi-, bahuvachana
        printf &ldquo;%-20s\t&rdquo;,
        sandhi(vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$i,vachana=&gt;$j}));
        }
     print &ldquo;\n&rdquo;;
     }
print &ldquo;\n&rdquo;;
</CODE></PRE><P>
USAGE: table_no_args.pl <P>
OUTPUT<BR>
<PRE></p>

<p>Table of all vibhakti/vachana combination for given noun/linga</p>

<p>Using noun raama, linga 1</p>

<p>rAmaH                   rAmau                   rAmAH<br />
rAmam                   rAmau                   rAmAn<br />
rAmeNa                  rAmAbhyAm               rAmaiH<br />
rAmAya                  rAmAbhyAm               rAmebhyaH<br />
rAmAt                   rAmAbhyAm               rAmebhyaH<br />
rAmasya                 rAmayoH                 rAmANAm<br />
rAme                    rAmayoH                 rAmeSu<br />
he rAma                 he rAmau                he rAmAH</p>

<p></PRE>
</BODY></HTML></p>
</div>
```
