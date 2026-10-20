---
title: "pratyay_no_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>pratyay_no_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(vibhakti);</p>

<p>print &ldquo;\nprints table of pratyay for given noun and linga\n&rdquo;;
print &ldquo;-kaar of linga is included in pratyay (internal sandhi)\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>my $noun=&ldquo;raama&rdquo;;   # a-kaarant
my $linga = 1;      # alias for &ldquo;puM&rdquo;;</p>

<p>print &ldquo;Using noun $noun, linga $linga\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>for my $i (1..8){   # prathamA through sambodhana
    for my $j (1..3){   # eka-, dvi-, bahuvachana
        my $pratyay =
            vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$i,vachana=&gt;$j});
        $pratyay =~ s/^.*+ //;     # remove the noun part
        printf &ldquo;%-10s\t&rdquo;,$pratyay;
        }
     print &ldquo;\n&rdquo;;
     }
print &ldquo;\n&rdquo;;
</CODE></PRE><P>
USAGE: pratyay_no_args.pl <P>
OUTPUT<BR>
<PRE></p>

<p>prints table of pratyay for given noun and linga
-kaar of linga is included in pratyay (internal sandhi)</p>

<p>Using noun raama, linga 1</p>

<p>aH          au          AH<br />
am          au          An<br />
eNa         Abhyaam     aiH<br />
Aya         Abhyaam     ebhyaH<br />
At          Abhyaam     ebhyaH<br />
asya        ayoH        ANaam<br />
e           ayoH        eSu<br />
a           au          AH</p>

<p></PRE>
</BODY></HTML></p>
</div>
```
