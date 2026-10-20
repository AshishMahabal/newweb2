#!/usr/local/bin/perl -w

&welcome;
&getargs;
&checkargs;
&whoseturn;
&displaypiles;
&makebits;
while(!$over){
	if($turn){&promptuser;}
	else{&execcompterm;}
	&deduct;
	&makebits;
#	&showbits;
	&displaypiles;
	&checkifover;
	}
#########################################################################
sub welcome{
print "This is NIM.\n\n";
print "Here there are a few piles with certain numbers\n";
print "Players take turns removing a non-negative number of items from\n";
print "any one pile. The one to lift the last item wins.\n\n";
print "Bugs, suggestions, cheques to Ashish Mahabal (aam\@astro.caltech.edu)\n\n";
}
#########################################################################
sub exitmessage{
print "USAGE: nim.pl piles [a b c ... piles]\nwhere a,b,c etc. are ints\n";
print "e.g. nim.pl 3 3 5 7\ni.e. 3 piles with 3, 5 and 7 items respectively.\n";
exit;
}
#########################################################################
sub getargs{
$piles=shift(@ARGV);
if(!$piles){&exitmessage;}
for($i=0;$i<$piles;++$i){$piles[$i]=shift(@ARGV);}
}
#########################################################################
sub checkargs{
for($i=0;$i<$piles;++$i){
while($piles[$i]>255 or $piles[$i]<1){
	print "Piles should contain between 1 and 255.\n";
	print "Pile $i contains $piles[$i]. Please input again: ";
	$piles[$i]=<STDIN>;
	}
}
}
#########################################################################
sub displaypiles{
print "\t\t\t\t\t\t\t\t";
$sigma=0;
for($i=0;$i<$piles;++$i){print "$piles[$i] ";$sigma+=$piles[$i];}
print "\n";
}
#########################################################################
sub whoseturn{
print "\n\nWill you play first? If not, type 0 ";
$turn=<STDIN>;
chop($turn);
#print "turn is $turn\n";
}
#########################################################################
sub promptuser{
$pilenum=$piles+1;
print "Your turn. ";
while($pilenum>=$piles){
	print "Input pile_number from which to remove (>0 and  <= $piles): ";
	$pilenum=<STDIN>;
	chop($pilenum);
	$pilenum=$pilenum-1;
	if($pilenum <=0 or !$piles[$pilenum]){
		$dummypile=$pilenum+1;
		print "Pile $dummypile does not exist. ";
		$pilenum=$piles+1;
		}
	}
$removeit=$piles[$pilenum]+1;
while($removeit>$piles[$pilenum]){
	print "Tell me how much I should remove (>0 and <= $piles[$pilenum]): ";
	$removeit=<STDIN>;
	if($removeit<=0){$removeit=$piles[$pilenum]+1;}
	}
	$turn=0;
}
#########################################################################
sub checkifover{
if(!$sigma){
	print "Game over. ";
	if(!$turn){print "You win\n";}else{print "I win\n";}
	$over=1;
	}
}
#########################################################################
sub makebits{
$checksum2=0;
for($j=0;$j<8;++$j){$checksum[$j]=0;}
for($i=0;$i<$piles;++$i){
	for($j=0;$j<8;++$j){
		$bits[$i][$j]=(($piles[$i]<<$j)>>7)%2; 
		$checksum[$j]+=$bits[$i][$j];
		}
	}
for($j=0;$j<8;++$j){$checksum[$j]%=2;$checksum2+=$checksum[$j];}
}
#########################################################################
sub showbits{
for($i=0;$i<$piles;++$i){
	for($j=0;$j<8;++$j){ print "$bits[$i][$j] ";}
	print "\n";
	}
}
#########################################################################
sub getrandom{
#	print @checksum;print "\n";
$pilenum=$#piles+1;
while(!$piles[$pilenum]){
$pilenum=int($piles*rand);
#print "$pilenum (pilenum with 0 counters)\n";
}
$removeit=1+int($piles[$pilenum-1]*rand);
#print "Was in random. ";
print "Removed $removeit from $pilenum\n";
}
#########################################################################
sub execcompterm{
#	print @checksum;print "\n";
for($j=0;$j<8;++$j){
	if($checksum[$j]){&findwhere;$j=10;}
	}
	if($j<10){&getrandom;}
	$turn=1;
}
#########################################################################
sub findwhere{
#print "j is $j\n";
#for($i=0;$i<$piles;++$i){print $bits[$i][$j];}print "\n";
for($i=0;$i<$piles;++$i){
	if($bits[$i][$j]){&findothers; $i=$piles;}
	}
}
#########################################################################
sub findothers{
#print "i and j are $i $j\n";
$sumtodiffer=0;
for($k=0;$k<8;++$k){
if(($checksum[$k] and !$bits[$i][$k]) or (!$checksum[$k] and $bits[$i][$k])){
		$thisval=2**(7-$k);
#		print "k is $k. Value is $thisval\n";
		$sumtodiffer+=$thisval;
		}
	}
$removeit=$piles[$i]-$sumtodiffer;
$pilenum=$i;
print "I am removing $removeit from $pilenum\n";
}
#########################################################################
sub deduct{
$piles[$pilenum]-=$removeit;
}
#########################################################################
