#!/usr/local/bin/perl -w

&help;
$width=8;
$remainingcols=$width;
generate_fibomarks(40);
@dispmap=(" ","\#","o","\*","\@","=","\%");
&play;
###########################
sub play{
local ($row,$col);
$level=3;
@tiles=();
$reftiles=\@tiles;
get_new_pattern($reftiles,$level);
$over=0;
$totalmarks=0;
$bestclear=0;
while(!$over){
	print "marks are $totalmarks\n";
	print_tiles($reftiles);
	unless(check_if_over($reftiles))
		{$over=1;print "\nSORRY GAME OVER\n";next;}
	print "choose tile (col): ";
	$col=(<STDIN>);
	chop($col);
	$col=$col-1;
	print "choose tile (row): ";
	$row=(<STDIN>);
	print "_____________________\n";
	chop($row);
	$row=$row-1;
	unless($$reftiles[$col][$row]>0){next;}
	if(get_neighbours($col,$row,$reftiles,$$reftiles[$col][$row],\@memlist)){
		collapse($reftiles,$remainingcols);
		$marks=$fibomarks[$#memlist];
		$totalmarks+=$marks;
		if($marks>$bestclear){$bestclear=$marks;}
		unless(zero($reftiles)){
			print "**********\nGREAT JOB\!\n**********\n";
			print "bonus marks: 5000\n";
			print "best clearing: $bestclear\n";
			$totalmarks+=5000+$bestclear*($level-2);
			print "total so far: $totalmarks\n";
			$level++;
			get_new_pattern($reftiles,$level);;
			$remainingcols=$width;
			}
	}
	}
}
###########################
sub check_if_over{
$reftiles=$_[0];
local ($row,$col);
for($row=0;$row<8;++$row){
	for($col=0;$col<8;++$col){
		if($$reftiles[$col][$row]>0){
	if(get_neighbours2($col,$row,$reftiles,$$reftiles[$col][$row]))
		{return 1;}
			}
		}
	}
	return 0;
}
###########################
sub collapse{
	local $matrix=$_[0];
	local ($col,$row);
	local $newrow;
	$remainingcols2=$_[1];

	for($col=0;$col<8;++$col){
		for($row=7;$row>=0;--$row){
			while($$matrix[$col][$row]==0){
				for($newrow=$row;$newrow>=0;--$newrow){
					$$matrix[$col][$newrow]=$$matrix[$col][$newrow-1];
				}
				$$matrix[$col][0]=-1;
			}

		}
	}
	for($col=0;$col<$remainingcols2;++$col){
		if($$matrix[$col][7]==-1){
			for($newcol=$col;$newcol<$remainingcols2-1;++$newcol){
			for($newrow=7;$newrow>=0;$newrow--){
				$$matrix[$newcol][$newrow]=$$matrix[$newcol+1][$newrow];
				}
			}
			for($newrow=7;$newrow>=0;$newrow--){
				$$matrix[$remainingcols2-1][$newrow]=-1;
				}
			--$remainingcols2;
			--$col;
		}
	}
}
########################
sub print_tiles{
	local $matrix=$_[0];
	local ($col,$row);
	print "row\n";
	for($row=0;$row<8;++$row){
		print $row+1;print "\|";
		for($col=0;$col<8;++$col){
			unless($$matrix[$col][$row]<0){
				print " $dispmap[$$matrix[$col][$row]]";
			}
else{
	print "  ";
}
		}
		print "\n";
	}
	print "   _______________\n";
	print "   1 2 3 4 5 6 7 8 col\n";
	print "\n";
}
########################
sub get_neighbours{
local $col=$_[0];
local $row=$_[1];
local $tileref=$_[2];
local $thistile=$_[3];
$refmemlist=$_[4];
local $check=0;
local $count=0;
@memlist=();
$refmemlist=\@memlist;
$$refmemlist[0]=$row*8+$col;
while($check<=$count){
	$col=$$refmemlist[$check]%$width;
	$row=int($$refmemlist[$check]/$width);
	$$tileref[$col][$row]=0;
	if($col > 0)
	{
		if(check_neighbour($col-1,$row,$tileref,$thistile))
		{ ++$count;$$refmemlist[$count]=$row*8+$col-1; }
	}
	if($col< $width-1)
	{
		if(check_neighbour($col+1,$row,$tileref,$thistile))
		{ ++$count;$$refmemlist[$count]=$row*8+$col+1; }
	}
	if($row>0)
	{
		if(check_neighbour($col,$row-1,$tileref,$thistile))
		{ ++$count;$$refmemlist[$count]=$row*8+$col-8; }
	}
	if($row< $width-1)
	{
		if(check_neighbour($col,$row+1,$tileref,$thistile))
		{ ++$count;$$refmemlist[$count]=$row*8+$col+8; }
	}
	++$check;
	}
	unless($count){$$tileref[$col][$row]=$thistile;}
	return $count;
}
########################
sub check_neighbour{
	local $col=$_[0];
	local $row=$_[1];
	local $tileref=$_[2];
	local $thistile=$_[3];
	if($$tileref[$col][$row] == $thistile){ 
		$$tileref[$col][$row]=0;
		return 1; 
		}
	else{return 0;}
}
########################
sub fibo{
	local $arg=$_[0];
	if($arg<=1){
		return 0;
	}
	elsif($arg<=4){
		return ($arg-1);
	}
else{
	$val=$fibomarks[$arg-2]+$fibomarks[$arg-3];
	return $val;
}
}
########################
sub generate_fibomarks{
	local $j=$_[0];
	local $i;
	for($i=0;$i<=$j;++$i){
		$fibomarks[$i]=fibo($i+1);
	}
}
########################
sub zero{
$reftiles=$_[0];
local ($col,$row);
local $count=0;
for($row=0;$row<8;++$row){
	for($col=0;$col<8;++$col){
		if($$reftiles[$col][$row]>0){++$count;}
		}
		}
return $count;
}
##############################
sub get_new_pattern{
$reftiles=$_[0];
local $level=$_[1];
local ($row,$col);
for($row=0;$row<8;++$row){
	for($col=0;$col<8;++$col){
		$$reftiles[$col][$row]=1+int($level*rand);
		}
	}			
}
##############################
sub get_neighbours2{
local $col=$_[0];
local $row=$_[1];
local $tileref=$_[2];
local $thistile=$_[3];
	if($col > 0)
	{
		if(check_neighbour2($col-1,$row,$tileref,$thistile))
		{ return 1; }
	}
	if($col< $width-1)
	{
		if(check_neighbour2($col+1,$row,$tileref,$thistile))
		{ return 1; }
	}
	if($row>0)
	{
		if(check_neighbour2($col,$row-1,$tileref,$thistile))
		{ return 1; }
	}
	if($row< $width-1)
	{
		if(check_neighbour2($col,$row+1,$tileref,$thistile))
		{ return 1; }
	}
return 0;
}
########################
sub check_neighbour2{
	local $col=$_[0];
	local $row=$_[1];
	local $tileref=$_[2];
	local $thistile=$_[3];
	if($$tileref[$col][$row] == $thistile){ 
		return 1; 
		}
	else{return 0;}
}
########################
sub help{
print <<EOP;
######################################
You are presented with a 8x8 matrix with 3+ different symbols.
Choose a symbol (by specifying its col and row) which has a similar symbol 
adjacent to it. The chosen symbol will vanish with all identical
adjacent symbols (and also their identical adjacent symbols). The more
you clear in one stroke, the more marks you get (in Fibonacci ordering:
1 for 2, 2 for 3 and then f(n-1)+f(n-2) for n. The game is over when
none of the remaining symbols has identical neighbours. When you clear the
board you get bonus marks and you are presented with a matrix with one
additional type of symbol.

bugs, cheques to aam\@astro.caltech.edu
Dec. 1999

All the best.
######################################

EOP
return;
}
########################
