#!/usr/local/bin/perl -w
# perl version of autosoup.c (in making)
$states=4;
$flibs=10;
$strleng=6;

#int e[strleng],chrom[flibs][states*4],score[flibs],state[flibs];

&initialise;
&print_environ_string;
&print_flib_states;
&print_flib_chromosomes;
while(++$steps){
  &count;
  &select_highlow;
  100*rand()<33?&cross:&mutate;
  } 
########################
sub initialise{
if(($ARGV[0]) eq "user"){
	print "input environ string (length 6, 0s and 1s separated by a space): ";
	$estring=<STDIN>;
	chop($estring);
	@e=split(" ",$estring);
	}
else{
for($i=0;$i<$strleng;++$i){
	$a=(rand()-0.5)*2;
#	print "a of rand is $a\n";
	if($a<0){$e[$i]=0;}else{$e[$i]=1;}
	}
}
for($i=0;$i<$flibs;++$i){
	$a=rand()*$states; $state[$i]=int($a);
#	print "a of rand*states is $a\n";
	}

for($i=0;$i<$flibs;++$i){ 
 for($j=0;$j<$states;++$j){
  $a=rand()-0.5;
  if($a<0){$chrom[$i][$j*4]=0;}
  else{$chrom[$i][$j*4]=1;}
  $a=rand()*$states; $chrom[$i][$j*4+1]=int($a);
  $a=rand()-0.5;
  if($a<0){$chrom[$i][$j*4+2]=0;}
  else{$chrom[$i][$j*4+2]=1;}
  $a=rand()*$states; $chrom[$i][$j*4+3]=int($a);
  }
 }
}
########################
sub count{
for($j=0;$j<$flibs;++$j){$score[$j]=0;}
for($i=0;$i<$strleng*2;++$i){
	$symb=$i%$strleng;
	for($j=0;$j<$flibs;++$j){
		$outsym=4*$state[$j]+2*$e[$symb];
		$state[$j]=$chrom[$j][$outsym+1];
		if($chrom[$j][$outsym]==$e[($symb+1)%$strleng]){++$score[$j];}
	      }
	}
}
########################
sub select_highlow{
$hi=0;$low=$strleng*2;
for($i=0;$i<$flibs;++$i){
      if($score[$i]>$hi){$hi=$score[$i];$hiflib=$i;}
      else{if($score[$i]<$low){$low=$score[$i];$lowflib=$i;}}
      }
#print "hi is $hi strleng is $strleng\n";
if($hi==$strleng*2){&output;}
}
########################
sub cross{
$a=rand()*($states*4);
$b=rand()*($states*4);
if($b<$a){$c=$a;$a=$b;$b=$c;}
$c=int(rand()*($flibs));
for($i=0;$i<$a;++$i){$chrom[$lowflib][$i]=$chrom[$hiflib][$i];}
for($i=$a;$i<$b;++$i){$chrom[$lowflib][$i]=$chrom[$c][$i];}
for($i=$b;$i<$states*4;++$i){$chrom[$lowflib][$i]=$chrom[$hiflib][$i];}
}
########################
sub mutate{
$a=int(rand()*($states*4));
$b=int(rand()*($flibs));
if(($a%2)==0){$chrom[$b][$a]=($chrom[$b][$a]+1)%2;}
else{$chrom[$b][$a]=($chrom[$b][$a]+1)%4;}
}
########################
sub output{
printf("\n\n\nA superior flib is born!\n");
printf(" No. %d in state %d with the config: ",$hiflib,$state[$hiflib]);
for($i=0;$i<$states*4;++$i){printf("%d ",$chrom[$hiflib][$i]);}
printf("\nThe required steps were %d",$steps);
printf("\nThe environ string was: ");
for($i=0;$i<$strleng;++$i){printf("%d ",$e[$i]);}
printf("\nThe scores for the flibs are: ");
for($i=0;$i<$flibs;++$i){printf("%d ",$score[$i]);}
&print_flib_chromosomes;
exit(0);
}
########################
sub print_flib_states{
printf("\nPrinting the flibs' states: ");
for($i=0;$i<$flibs;++$i){printf("%d",$state[$i]);}
}
########################
sub print_flib_chromosomes{
printf("\nThe flib chromosomes are: \n\n");
for($i=0;$i<$flibs;++$i){	
	for($j=0;$j<$states*4;++$j){printf("%d ",$chrom[$i][$j]);}
	printf("\n");
}
}
########################
sub print_environ_string{
printf("\nThe environment string is: \n");
for($i=0;$i<$strleng;++$i){printf("%d ",$e[$i]);}
}
########################
#sub rand{
#return rand;
#}
########################
