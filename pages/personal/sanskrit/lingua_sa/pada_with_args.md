---
title: "pada_with_args.pl"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/sanskrit/">Sanskrit</a> › <a href="/personal/sanskrit/lingua_sa/">Lingua SA</a></p>
<h1>pada_with_args.pl</h1>
<div class="legacy">
<p><HTML><BODY>
<PRE><CODE>
use strict;
use Carp;
use Lingua::SA qw(sandhi vibhakti);</p>

<p>#USAGE: perl $0 raama puM prathamA ekavachana</p>

<h1 id="or">or</h1>

<p>#USAGE: perl $0 raama puM 1 ekavachana</p>

<h1 id="etc">etc.</h1>

<p>my ($noun,$linga,$vibhakti,$vachana) = @ARGV;
unless(defined $noun and defined $linga and defined $vibhakti and defined $vachana){
        croak &ldquo;Please provide noun, linga, vibhakti, vachana as args&rdquo;;
        }</p>

<p>print &ldquo;\nprints desired pada for given noun, linga, vibhakti, vachana\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>print &ldquo;Using provided noun $noun, linga $linga, vibhakti $vibhakti, vachana $vachana\n&rdquo;;
print &ldquo;\n&rdquo;;</p>

<p>my $pada =
sandhi(vibhakti({naam=&gt;$noun,linga=&gt;$linga,vibhakti=&gt;$vibhakti,vachana=&gt;$vachana}));
print &ldquo;$pada\n\n&rdquo;;
</CODE></PRE><P>
USAGE: pada_with_args.pl raama puM 1 ekavachana<P>
OUTPUT<BR>
<PRE></p>

<p>prints desired pada for given noun, linga, vibhakti, vachana</p>

<p>Using provided noun raama, linga puM, vibhakti 1, vachana ekavachana</p>

<p>rAmaH</p>

<p></PRE>
</BODY></HTML></p>
</div>
```
