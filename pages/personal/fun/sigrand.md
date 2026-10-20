---
title: "Random Signatures"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/fun/">Fun</a></p>
<div class="legacy">
<P CLASS=top>
<IMG src="/images/name.jpg" align=left height=40>
<IMG src="/images/logo.jpg" align=right height=40>
<BR>
<HR>
</P>
<CENTER><H2>Random Signatures</H2></CENTER>
<P>
I use Pine to send and read email. Here I highlight the use of
a program (sigrand) which allows
you to use a random signature per pine session from a preselected set.
<P>
The program essentially rewrites a named file periodically, and hence 
could be used with any mail reader which reads the signature from a file.
<P>
<OL>
<LI> Create a file called ~/NEWS/SIGNATURES (the name is configurable)<BR>
<LI> Populate it with lines/paragraphs separated by %%, thus:
<PRE>
Signatures are a waste of bandwidth.
%%
Help stamp out signatures.
%%
'Calm down -- it's only ones and zeros.'
%%
According to my calculations the problem doesn't exist.
%%
</PRE>
<LI> Run <A href="/personal/fun/sigrand.pl">sigrand.pl</a>. It keeps running in the 
background and uses FIFO. Thus you have to run it everytime you reboot.
<LI>Use an alias to read the named pipe viz. r to write to your signature
file and use it in the mail program e.g.:
<PRE>
alias mail      'cat ~/r >! ~/.signature;pine -i -f INBOX;date'
</PRE>
</OL>
<P>
The program can do much more and is all yours to explore.
Good luck and drop me a line if it works out. I could be a little slow in replying queries, but will get back to them.
<P>
Ah, and a word of advice: keep the total length of each of your signatures
below four 80 character lines. Please.
<P>
And of course, the program will work sensibly only on sensible OSes viz. *N*X
<HR>
<I>sigrand</I> is from the perl cookbook (Christiansen and Torkington, O'Reilly).
<P CLASS=bottomline>
<TABLE CLASS=snug WIDTH=100% CELLBORDER=0 CELLSPACING=0>
<TR>
<TD WIDTH=20%>
<A href="/science/research.html">Science</a>
</TD>
<TD WIDTH=20%>
<A href="/personal/fun/fun/">Fun</a>
</TD>
<TD WIDTH=20%>
<A href="/philosophy/philosophy.html">Philosophy</a>
</TD>
<TD WIDTH=20%>
<A href="/personal/personal.html">Personal</a>
</TD>
<TD WIDTH=20%>
<A href="/miscellaneous/miscellaneous.html">Miscellaneous</a>
</TD>
</TR>
</TABLE>
</P>
<H6 CLASS=email><A HREF="mailto::aam@astro.caltech.edu">Ashish Mahabal</a>
<BR>
Last Outdated: Nov 15 2001
</H6>
<CENTER><H7 CLASS=absbottom>
http://www.astro.caltech.edu/~aam/fun/sigrand.html
</H7></CENTER>
</div>
```
