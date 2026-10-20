---
title: "pratyay_with_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>pratyay_with_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(vibhakti);</p>

<h1 id="usage-perl-0-raama-pum">USAGE perl $0 raama puM</h1>

<h1 id="or">or</h1>

<h1 id="usage-perl-0-raama-1">USAGE perl $0 raama 1</h1>

<h1 id="etc">etc.</h1>

<p>my ($noun,$linga) = @ARGV;
unless(defined $noun and defined $linga){
        croak &ldquo;Please provide noun and linga as args&rdquo;;
        }</p>

<p>print &ldquo;\nprints table of pratyay for given noun and linga\n&rdquo;;
print &ldquo;-kaar of linga is included in pratyay (internal sandhi)\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>print &ldquo;Using provided noun $noun, linga $linga\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>for my $i (1..8){   # prathamA through sambodhana
    for my $j (1..3){   # eka-, dvi-, bahuvachana
        my $pratyay =
            vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$i,vachana=&gt;$j});</p>

<h1 id="pratyay-s-remove-the-noun-part">$pratyay =~ s/^.*+ //;     # remove the noun part</h1>
<pre><code>    $pratyay =~ s/[a-zA-Z]* \+ //g;     # remove the noun part
    if($i==8){$pratyay =~ s/^he //;}    # remove the sambodhan
    printf &#34;%-10s\t&#34;,$pratyay;
    }
 print &#34;\n&#34;;
 }</code></pre>
<p>print &ldquo;\n&rdquo;;
</CODE></PRE><P>
USAGE: pratyay_with_args.pl raama 1<P>
OUTPUT<BR>
<PRE></p>

<p>prints table of pratyay for given noun and linga
-kaar of linga is included in pratyay (internal sandhi)</p>

<p>Using provided noun raama, linga 1</p>

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
