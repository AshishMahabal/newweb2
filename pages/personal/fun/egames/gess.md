---
title: "Gess, what?"
---

```{=html}
<p class="back-link"><a href="/personal/">Personal</a> › <a href="/personal/fun/">Fun</a> › <a href="/personal/fun/egames/">egames</a></p>
<div class="legacy">
Gess is the combination of Go and Chess. It has very simple rules 
and yet it can be tricky to play. I present here a Java applet that allows
you to play gess with yourself or with a friend sitting next to you.
<P>
The program, tells you when one side has lost, but allows you to continue
playing anyway so that you can try out different steps. Until I rectify
it, treat it as a feature.
<P>
Rules:<BR>
<UL>
<LI>It is played on a standard 18x18 Go board with a "twilight zone" on either
side making it a <A href="/personal/fun/egames/images/board.gif" WIDTH=200 HEIGHT=200>20x20 board</a>
(a--t, 1--20 where columns a and t and rows 1
and 20 cannot be occupied by stones).
<LI>Each player has 43 stones. Red goes first.
<LI>A piece is defined by a 3x3 region not containing your opponents stones
and with at least one of your stone being along the periphery.
<TABLE>
<TR>
<TH>Rook</TH>
<TH>Bishop</TH>
<TH>Queen</TH>
<TH>Ring</TH>
<TH>Pawn</TH>
<TH>Hybrid1</TH>
<TH>Hybrid2</TH>
<TH>Hybrid3</TH>
<TH>Hybrid4</TH>
<TH>Partly twilight</TH>
</TR>
<TR>
<TD><IMG src="/personal/fun/egames/images/rook.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/bishop.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/queen.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/ring.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/pawn.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/hybrid1.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/hybrid2.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/hybrid3.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/hybrid4.gif" WIDTH=30 HEIGHT=30></TD>
<TD><IMG src="/personal/fun/egames/images/partly_twilight.gif" WIDTH=30 HEIGHT=30></TD>
</TR>
</TABLE>
<LI>If the middle square of you 3x3 piece is occupied, the piece can move
until obstructed. Otherwise it can move at most three steps.
<LI>If obstructed, the piece stops there. Stones which were there earlier
go out.
<LI>One can remove ones own stones in the above fashion.
<LI>The "twilight zone" can be used as part of a 3x3 piece. But any stone
that goes on to it vanishes off the board.
<LI>Each player has a ring to begin with: a 3x3 piece with the center empty.
You lose when you lose your ring. You can accumulate more rings during the play.
</UL>
<P>
<A href="/personal/fun/egames/gessgame/">Enjoy the game!</a>
</div>
```
