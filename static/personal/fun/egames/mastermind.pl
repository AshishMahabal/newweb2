#!/usr/local/bin/perl -w
#This is the game where you display your masterfulness
#by guessing a code.
&welcome;
&initialize;
&turns;
&saysorry;
sub welcome{
print "\n\n";
print "Brainwave or mastermind, the standard version.\n\n";
print "Bugs, suggestions, cheques to aam\@astro.caltech.edu\n\n";
print "6 colors viz. K B R Y G W for blacK Blue Red Yellow Green White\n";
print "I will choose a set of four and you have 10 guesses\n";
print "Enter your guesses as: R R B Y\n";
}
sub initialize{
@C=('K', 'B', 'R', 'Y', 'G', 'W');
for($i=0;$i<4;++$i){
	$X[$i]=$C[int(6*rand)];
	$X1[$i]=0;$Y1[$i]=0;	#Default actually!
	}
#	print @X,"\n";
}
sub turns{
print "On to the 10 turns:\n";
MAINLOOP: for($j=0;$j<10;++$j){
	$guess=$j+1;
	print "Input your guess ( $guess ) \n";
	$B[$j]=0; $W[$j]=0;
	for($i=0;$i<4;++$i){$X1[$i]=0;$Y1[$i]=0;}
	$input[$j]=<STDIN>;
	chop($input[$j]);
	@A=split(' ',$input[$j]);
	for($i=0;$i<4;++$i){
		$Y[$i]=-1;
		for($k=0;$k<6;++$k){if($A[$i] eq $C[$k]){$Y[$i]=$k;}}
		unless($Y[$i]>=0){
			print "Invalid entry.\n";
			redo MAINLOOP;
			}
		}
#		print @Y;
	for($i=0;$i<4;++$i){
#		print $X[$i],$C[$Y[$i]],"\n";
		if($X[$i] eq $C[$Y[$i]]){++$B[$j]; $X1[$i]=1;$Y1[$i]=1;}
		}
WHITELOOP:	for($i=0;$i<4;++$i){
		if($X1[$i]==0){
			for($k=0;$k<4;++$k){
				if($Y1[$k]==0){
					if($C[$Y[$k]] eq $X[$i]){
						++$W[$j];$Y1[$k]=1;$X1[$i]=1;
						next WHITELOOP;
						}
					}
				}
			}
		}
	print "\t\tYou got $B[$j] blacks and $W[$j] whites\n";
	print "Situation so far:\n   Try   B W\n--------------\n";
	for($l=0;$l<=$j;++$l){print "$input[$l]  $B[$l] $W[$l]\n";}
	print "\n";
	if($B[$j]==4){
		print "\n\nCongrats, you got it! @X ";
		print "You took $guess steps\n";
		exit;
		}
	}
}
sub saysorry{
print "Sorry, you had your 10 chances. It was @X\n";
}
