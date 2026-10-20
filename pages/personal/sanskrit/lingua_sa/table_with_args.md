---
title: "table_with_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>table_with_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(sandhi vibhakti);</p>

<h1 id="usage-perl-0-raama-pum">USAGE: perl $0 raama puM</h1>

<h1 id="or">or</h1>

<h1 id="usage-perl-0-raama-1">USAGE: perl $0 raama 1</h1>

<h1 id="etc">etc.</h1>

<p>my ($noun,$linga) = @ARGV;
unless(defined $noun and defined $linga){
    croak &ldquo;Please provide noun and linga as args&rdquo;;
    }</p>

<p>print &ldquo;\nTable of all vibhakti/vachana combination for given noun/linga\n&rdquo;;
print &ldquo;Using provided noun $noun, linga $linga\n\n&rdquo;;</p>

<p>for my $i (1..8){
    for my $j (1..3){
        printf &ldquo;%-20s\t&rdquo;,
        sandhi(vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$i,vachana=&gt;$j}));
        }
     print &ldquo;\n&rdquo;;
     }
print &ldquo;\n&rdquo;;
</CODE></PRE><P>
USAGE: table_with_args.pl raama 1<P>
OUTPUT<BR>
<PRE></p>

<p>Table of all vibhakti/vachana combination for given noun/linga
Using provided noun raama, linga 1</p>

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
