#!/usr/bin/perl -w -CSio

#
#  Copyright 2012,2013,2014 transLectures-UPV Team
#  Copyright 2009,2010,2011 Isaías Sánchez Cortina
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Spanish Syllable separator...
# by Isaias Sanchez Cortina . isanchez@dsic.upv.es . March 2012
# The only script which sumarizes the 11 spanish separation rules into one (regexp)
use strict "vars"; 
use Encode;
use POSIX;
use utf8;

our $DEBUG=0;
our $BOOL_TildeAccentedSyllables=1;
our $BOOL_AFI=0;
our $BOOL_SIMPLE=0;
our $BOOL_EUTRANSCRIBE=0;
our $BOOL_lowercase=1;
our $TOKEN_longsilence=" sil ";
our $TOKEN_shortpause=" ";
our $TOKEN_silence=" sp ";
our $BOOL_PrintAsSeparatedPhonemes=0;
our $BOOL_iAtrosLX=0;
our $BOOL_HTKDict=0;
our $BOOL_RegexLike=0;
our $RegexLikeDelete;
our $RegexLike; 
our $RegexLikeSF;
our $RegexLikeMMM;
our $BOOL_PrintWordNotRegexInLX=0;

# SPANISH SYLLABLE SEPARARTOR
our $aeo=decode_utf8(encode_utf8("áéó"));
our $ae=decode_utf8(encode_utf8("áé"));
our $u=decode_utf8(encode_utf8("ü"));
our $iu="[".decode_utf8(encode_utf8("íú"))."]";
our $a=decode_utf8(encode_utf8("á"));
our $e=decode_utf8(encode_utf8("é"));
our $i=decode_utf8(encode_utf8("í"));
our $o=decode_utf8(encode_utf8("ó"));
our $uu=decode_utf8(encode_utf8("ú"));

my $v=decode_utf8(encode_utf8("aeiouáéíóúäëïöüâêîôûàèìòùy"));
our $V="[$v]"; #Vowels
our $nonV="[^$v]"; #Vowels
our $VV="([aeo$aeo$i$uu]h?[uiy]|[ui$u]h?[aeoui$aeo$i$uu])";# Diftongs
our $VVV="([ui$u]h?[ae$ae]h?[uiy])"; #Triptongs
our $W="($VVV|$VV|$V)";
our $C="[".decode_utf8(encode_utf8("çßbcdfghjklmnñpqrstvwxYzABCDEFGHIJKLMNOPQR"))."]";
# Input must be lowercased
our $tilded="[".decode_utf8(encode_utf8("àèìòùáéíóú"))."]";

# Non-Spanish Tildes
our %NonSpanishTildes=('à'=>'á', 'è'=>'é', 'ì'=>'í', 'ò'=>'ó' ,'ù'=>'ú', 
		      'â'=>'a', 'ê'=>'e', 'î'=>'i', 'ô'=>'o' ,'û'=>'u');
our $STR_REGEX_NonSpanishTildes= '('.join('|',keys(%NonSpanishTildes)).')'; 
our $REGEX_NonSpanishTildes=qr/$STR_REGEX_NonSpanishTildes/o;
# Spanish Tilded vowels to be converted to plain vowels
our %SpanishTildes=($a=>'a', $e=>'e', $i=>'i', $o=>'o' ,$uu=>'u' , 
        decode_utf8(encode_utf8('à')) => 'a' , decode_utf8(encode_utf8('è')) => 'e'  , decode_utf8(encode_utf8('ì')) => 'i'  , decode_utf8(encode_utf8('ò')) => 'o'  , decode_utf8(encode_utf8('ù')) => 'u' , decode_utf8(encode_utf8('ỳ')) => 'y'   ,
        decode_utf8(encode_utf8('ä')) => 'a' , decode_utf8(encode_utf8('ë')) => 'e'  , decode_utf8(encode_utf8('ï')) => 'i'  , decode_utf8(encode_utf8('ö')) => 'o'  , decode_utf8(encode_utf8('ü')) => 'u' , decode_utf8(encode_utf8('ÿ')) => 'y'   ,
        decode_utf8(encode_utf8('â')) => 'a' , decode_utf8(encode_utf8('ê')) => 'e'  , decode_utf8(encode_utf8('î')) => 'i'  , decode_utf8(encode_utf8('ô')) => 'o'  , decode_utf8(encode_utf8('û')) => 'u' , decode_utf8(encode_utf8('ŷ')) => 'y'   );
our $STR_REGEX_SpanishTildes= "(".join("|",keys(%SpanishTildes)).")"; 
our $REGEX_SpanishTildes=qr/$STR_REGEX_SpanishTildes/o;
# Spanish transcription of consonants in abecedary:
our %STR_Abecedary=(
'a' => 'a' , 'b' => 'be' , 'c' => 'ce' , 'd' => 'de' , 'e' => 'e' , 'f' => 'efe' , 
'g' => 'ge' , 'h' => 'haPe' , 'i' => 'i' , 'j' => 'jota' , 'k' => 'ca' , 'l' => 'ele' , 
'm' => 'eme' , 'n' => 'ene' , 'ñ' => 'eñe' , 'o' => 'o' , 'p' => 'pe' , 'q' => 'cu' , 
'r' => 'eOe' , 's' => 'ese' , 't' => 'te' , 'u' => 'u' , 'v' => 'uve' , 'w' => 'uvedoBe' , 
'x' => 'eQis' , 'y' => 'iHiega' , 'z' => 'zeta', 'ch' => 'Pe' , 'ç' => 'cediKa',
'A' => 'beeOe' ,  
 'B' => 'beele' ,
 'C' => 'ceeOe' ,
 'D' => 'ceele' ,
 'E' => 'deeOe' ,
 'F' => 'efeeOe' ,
 'G' => 'efeeLe' ,
 'H' => 'geeOe' ,
 'I' => 'gele' ,
 'J' => 'caeOe' ,
 'K' => 'eye' ,
 'L' => 'peeOe' ,
 'M' => 'peele' ,
 'N' => 'teeOe' ,
 'O' => 'eRedoBe' ,
 'P' => 'Pe' ,
 'Q' => 'cu' ,
 'R' => 'gu' ,
 'S' => 'doBeese' ,
 'Y' => 'iHiega'
);

our $f=decode_utf8(encode_utf8("ɟ"));
our $j=decode_utf8(encode_utf8("ʝ"));
our $tS=decode_utf8(encode_utf8("ʧ"));
our $d3=decode_utf8(encode_utf8("ʤ"));
our $theta=decode_utf8(encode_utf8("θ"));
our $shaua=decode_utf8(encode_utf8("ʃ"));
our $zep=decode_utf8(encode_utf8("ʒ"));
our $s=decode_utf8(encode_utf8("ʂ"));
our $z=decode_utf8(encode_utf8("ʐ"));
our $X=decode_utf8(encode_utf8("χ"));
our $beta=decode_utf8(encode_utf8("β"));#
our $minv=decode_utf8(encode_utf8("ɰ"));
our $enye=decode_utf8(encode_utf8("ɲ"));
our $letraenye=decode_utf8(encode_utf8("ñ"));
our $ndent=decode_utf8(encode_utf8("ŋ"));
our $N=decode_utf8(encode_utf8("ɴ"));
our $r=decode_utf8(encode_utf8("ɾ"));
our $lambda=decode_utf8(encode_utf8("ʎ"));
our $m=decode_utf8(encode_utf8("ɱ"));

# 2 char wides depending on font / 2 chars unicode
our $t=decode_utf8(encode_utf8("t̪"));
our $delta=decode_utf8(encode_utf8("ð̞"));
our $d=decode_utf8(encode_utf8("d̪"));
our $jdot=decode_utf8(encode_utf8("ʝ̞"));
our $l=decode_utf8(encode_utf8("l̪"));
our $l1=decode_utf8(encode_utf8("lʲ"));
our $n=decode_utf8(encode_utf8("n̪"));
our $ndot=decode_utf8(encode_utf8("n̟"));
our $n1=decode_utf8(encode_utf8("nʲ"));

# our $t=decode_utf8(encode_utf8("t"));
# our $delta=decode_utf8(encode_utf8("ð"));
# our $d=decode_utf8(encode_utf8("d"));
# our $jdot=decode_utf8(encode_utf8("ʝ"));
# our $l=decode_utf8(encode_utf8("l"));
# our $l1=decode_utf8(encode_utf8("l"));
# our $n=decode_utf8(encode_utf8("n"));
# our $ndot=decode_utf8(encode_utf8("n"));
# our $n1=decode_utf8(encode_utf8("n"));

while(@ARGV){
  $_=shift(@ARGV);
  /^--?h(elp)$/ && (  help() );
  /^\+RegexLike$/ && ($BOOL_RegexLike=1, next); 
  /^\+PrintWordNotRegexInLX/  && ($BOOL_PrintWordNotRegexInLX=1,next); 
  /^\+iAtrosLX$/ && ($BOOL_PrintAsSeparatedPhonemes=1, $BOOL_EUTRANSCRIBE=1, $BOOL_TildeAccentedSyllables=0, $TOKEN_shortpause=' ', $TOKEN_silence=' ', $BOOL_iAtrosLX=1, next);
  /^\+HTKDict$/ && ($BOOL_PrintAsSeparatedPhonemes=1, $BOOL_EUTRANSCRIBE=1, $BOOL_TildeAccentedSyllables=0, $TOKEN_shortpause=' ', $TOKEN_silence=' ', $BOOL_HTKDict=1, next);
  /^-t$/ && ($BOOL_TildeAccentedSyllables=0, next) ;
  /^-g$/ && ($DEBUG=1, next) ;
  /^\+AFI$/ && ($BOOL_AFI=1, next);
  /^\+SIMPLE$/ && ($BOOL_SIMPLE=1, next);
  /^\+EUTRANSCRIBE$/ && ($BOOL_EUTRANSCRIBE=1, next);
  #/^--originalcase/ && ($BOOL_lowercase=0,next);
  /^-sp$/ && ($TOKEN_shortpause=' ', next);
  /^-sil$/ && ($TOKEN_silence=' ', next);
  /^-longsil$/ && ($TOKEN_longsilence=' ', next);
  /^--sp$/ && ($TOKEN_shortpause=shift || help(), next);
  /^--sil$/ && ($TOKEN_silence=shift || help(), next);
  /^--longsil$/ && ($TOKEN_longsilence=shift || help(), next);
  /^\+c$/ && ($BOOL_PrintAsSeparatedPhonemes=1, next) ;
   print STDERR "$0 : Unknown Option '$_'\n"; 
   help();
}

if ($BOOL_RegexLike){
	$RegexLikeMMM=qr/\/m+\/([^\/]*)\//i;
	$RegexLike=qr/\/([^\/]*)\/([^\/]*)\//;
	$RegexLikeSF=qr/\/SF\/([^\/]*)\//i;
}

while  (<>){
	study;
  s/\s*$//;
  s/^\s*+//g;
  print "$_ 1.0 " if $BOOL_iAtrosLX;
  print "$_ " if $BOOL_HTKDict;
  if ($BOOL_RegexLike){
	s/$RegexLikeSF/./g; # /SF// => . , so this will be transliterated to 'sil' by default.
	s/$RegexLikeMMM/mmm/g; # Prevents /mmm/*// to be transliterated to 'eme eme eme' , instead symbol Z will be mapped to 'm' 
	s/$RegexLike/$1/g; # /actual non-normative utterance/ortographic intended word/ => actual non-normative utterance
  }

  $_=lc if $BOOL_lowercase;

  # Underscores to blank
  s/_+/ /g; 
  # acentuaciones de caracteres no castellanos
  s/$REGEX_NonSpanishTildes/$NonSpanishTildes{$1}/g;
  
  # Numbers to Words
  my $line=$_;
  while ($line =~ m/([0-9]+)/gc){
    my $p=pos($line);
    my $numb=$1;
    my $l=length($numb);
    my $num=Number2Words($numb);
    print STDERR "$0: Substituting number $numb found at ", $p-$l," of length $l by $num on $line\n"  if  $DEBUG; 
    substr $line,$p-$l,$l," $num";		
  }
  
  $_=$line;
  # abreviaturas
  s/\s+/ /g;
  s/nº/numero/g;
  s/mª/maria/g;
  s/º/primero/g;
  s/ª/primera/g; 
  s/\@/ arroba /;
  s/\%/por ciento/;
  s/\'//g;
  # RULE 2:  Hay grupos de consonantes inseparables => temporary substitution
   s/br/A/g ;
   s/bl/B/g ;
   s/cr/C/g ;
   s/cl/D/g ;
   s/dr/E/g ;
   s/fr/F/g ;
   s/fl/G/g ;
   s/gr/H/g ;
   s/gl/I/g ;
   s/kr/J/g ;
   s/ll/K/g ;
   s/pr/L/g ;
   s/pl/M/g ;
   s/tr/N/g ;
   s/(^|\s)\Kr(?=$W)/O/g;
   s/rr+/O/g ;
   s/ch/P/g ;
   s/qu/Q/g ;
   s/gu([ei])/R$1/g ;
   s/ss/S/g ;
  # Consonant Y
   s/$C\Ky/i/g;
   s/y++(?=$W)/Y/g;

  @_=split(/([\~\.\,-:;\{\}\'\¨\^\`\*\+\[\]\!\|\"\·\$\%\&\/\(\)\=\?\¿\@\#\¬\'\¡\<\>\\\s]+)/);  
#   my $patternacute="[ns$V]"; 
  while (@_){ # For ech word at a certain line ...
    $_=shift(@_);
    if (/([\~\.\,-:;\{\}\'\¨\^\`\*\+\[\]\!\|\"\·\$\%\&\/\(\)\=\?\¿\@\#\¬\'\¡\<\>\\]+)/) {
      print $TOKEN_longsilence;
      next;
    }
    next if /\s/;
    print STDERR "\nSplit '$_' into Syllables : " if $DEBUG;
    # has tilde?
    my $hastilde=0;
    $hastilde=1 if /$tilded/ ; 

    # split into syllables
    my @Syl=();

   while ($_) {
      print STDERR "parsing '$_' " if $DEBUG;
      if ( (s/^($C*$W$C+)(?=$C$W|$)//) || (s/^($C*$W)(?=$C?$W|$)//)  ){
         push @Syl, $1;
         print STDERR "...(OK) added '$1' " if $DEBUG;
         next;
      } else {
         print STDERR "...(ERROR) " if $DEBUG;
         if ($BOOL_AFI || $BOOL_SIMPLE || $BOOL_EUTRANSCRIBE ) { 
	    if ($_ =~ /m+/) {
		push @Syl, 'm';
		print STDERR "...(OK) added excepcion mmm to m\n" if $DEBUG;
		last
	     }
            print STDERR " spelling " if $DEBUG;
            my @STR_tmp;
            for my $char (split('',$_)) {
               print STDERR " '$char': " if $DEBUG;
               my $char_spelling=$STR_Abecedary{$char};
               if (defined($char_spelling))  {
                  push  @STR_tmp, $char_spelling;
                  print STDERR " ... added $char_spelling " if $DEBUG;
               } else {
                  #push @STR_tmp , $TOKEN_silence ;
                  print STDERR " ... (UNKNOWN) supressed $char " if $DEBUG;
               }
            }
            $_=join('',@STR_tmp);
         } else {
            push @Syl, $_;
            print STDERR " added as is '$_' " if $DEBUG;
            last;
         }
      }
   }
   print STDERR "\n" if $DEBUG;
    #Tilde if untilded and has more than one syllable
    my $p=$#Syl;
    if ($BOOL_TildeAccentedSyllables && ($hastilde==0)&&($p>0) ){
      # Decide wheather it is acute or plain accented
      # if it ends with vowel or n or s, and it has no tilde,
      # then it is plain-accented:
      #Try to tilde an non-closed vowel. Then the first 
      # ex: ahuyentar: ahu yén tar
      # ex caminan: ca mí nan	    
      $p-- if ($Syl[$p] =~ /[aeiouyns]$/) ;
      # tilde on open vowels if any. 
      $Syl[$p] =~ (($Syl[$p] =~ s/i$/$i/ ) ||($Syl[$p] =~ s/u$/$uu/ )) unless (($Syl[$p] =~ s/a/$a/ ) ||($Syl[$p] =~ s/e/$e/ ) ||($Syl[$p] =~ s/o/$o/ ));
    }
    
    our $ss=decode_utf8(encode_utf8("ß"));
    # print separated tilded syllables
    for my $i (0 .. $#Syl) {
      $_=$Syl[$i];
      s/A/br/g ;
      s/B/bl/g ;
      s/C/cr/g ;
      s/D/cl/g ;
      s/E/dr/g ;
      s/F/fr/g ;
      s/G/fl/g ;
      s/H/gr/g ;
      s/I/gl/g ;
      s/J/kr/g ;
      s/K/ll/g ;
      s/L/pr/g ;
      s/M/pl/g ;
      s/N/tr/g ;
      s/O/rr/g ;
      s/P/ch/g ;
      s/Q/qu/g ;
      s/R/gu/g ;
      s/S/ss/g ;
      #ending y is a vowel
      s/Y+/y/g;
      $_=SpanishAFIPhones($_) if $BOOL_AFI;
      $_=SpanishSIMPLEPhones($_) if $BOOL_SIMPLE;
      $_=SpanishEUTRANSCRIBEPhones($_) if $BOOL_EUTRANSCRIBE;
      # PATCH: Convert tilded-vowels to plain (when explictly requested)
      s/$REGEX_SpanishTildes/$SpanishTildes{$1}/g unless ($BOOL_TildeAccentedSyllables);
      $_=join(" ", split ('', $_)) if $BOOL_PrintAsSeparatedPhonemes;
      s/$ss/s/g;
      $Syl[$i]=$_;
    }
    print join($TOKEN_shortpause,@Syl).$TOKEN_silence;

  }
  print "\n";
}

sub help{

    print STDOUT <<EOF;
\e[1mHELP\e[0m
________________________________________________________________________________
    Splits words into syllables, following spanish rules.
Text should be supplied by the standard input.
________________________________________________________________________________
OPTIONS:
 Text case:
  -originalcase   : Do not lowercase the text.
  -t              : Do not tilde resulting syllables or phonemes.
 Phoneme transliteration schemes: 
  +AFI            : Convert to phonemes using stardard UTF-8 AFI symbols
  +SIMPLE         : Convert to phonemes using ASCII
  +EUTRANSCRIBE   : Same as +SIMPLE but /$tS/ => 'c'. /r/ => '\@'
 Silences:
  -sp             : Do not add a token between syllables (default)
  -sil            : Do not add a token between words
  -longsil        : Do not add a token for punctuation symbols
  --sp TOKEN      : Add TOKEN between syllables (default: ' ')
  --sil TOKEN     : Add TOKEN between words (default: ' sp ')
  --longsil TOKEN : Add TOKEN between for punctuation symbols (default: ' sil ')
  Split:
  +c              : Split characters.
 Output format:
  +iAtrosLX       : Sets +c -t +EUTRANSCRIBE -sp -sil and
                    Outputs in iAtros Lexicon/dictionary format:
                    [word 1.0 /ascii phonetic transliteration/]
  +HTKDict        : Sets +c -t +EUTRANSCRIBE -sp -sil and
                    Outputs in HTK Lexicon/dictionary format:
                    [word /ascii phonetic transliteration]/\n

________________________________________________________________________________
Phoneme Transliteration Scheme for Spanish                                      
+AFI (Asociación Fonética Internacional)________________________________________
$f = /ɟ/  $j = /ʝ/  $tS = /ʧ/  $d3 = /ʤ/  $theta = /θ/  $shaua = /ʃ/  $zep = /ʒ/  $s = /ʂ/
$z = /ʐ/  $X = /χ/  $beta = /β/  $minv = /ɰ/  $letraenye = /ñ/  $ndent = /ŋ/  $N = /ɴ/  $r = /ɾ/
$lambda = /ʎ/  $m = /ɱ/  $t = /t̪/  $delta = /ð̞/  $d = /d̪/  $jdot = /ʝ̞/  $l = /l̪/  $l1 = /lʲ/
$lambda = /ʎ/  $n = /n̪/  $ndot = /n̟/  $n1 = /nʲ/ $enye = /ɲ/
+SIMPLE      ___________________________________________________________________
f = /ɟ/  i = /ʝ/  C = /ʧ/  z = /θ/  s = /ʃ/  s = /ʒ/  s = /ʂ/ 
s = /ʐ/  x = /χ/  b = /β/  m = /ɰ/  n = /ŋ/  n = /ɴ/  r = /ɾ/  R = /r/
y = /ʎ/  m = /ɱ/  t = /t̪/  d = /ð̞/  d = /d̪/  y = /ʝ̞/  l = /l̪/  l = /lʲ/
n = /n̪/  n = /n̟/  n = /nʲ/ h = /ɲ/
+EUTRANSCRIBE___________________________________________________________________
f = /ɟ/  i = /ʝ/  c = /ʧ/  z = /θ/  s = /ʃ/  s = /ʒ/  s = /ʂ/ 
s = /ʐ/  x = /χ/  b = /β/  m = /ɰ/  n = /ŋ/  n = /ɴ/  r = /ɾ/  \@ = /r/
y = /ʎ/  m = /ɱ/  t = /t̪/  d = /ð̞/  d = /d̪/  y = /ʝ̞/  l = /l̪/  l = /lʲ/
n = /n̪/  n = /n̟/  n = /nʲ/ h = /ɲ/
                                         _______________________________________
                                       v1.122 isanchez\@dsci.upv.es (March 2013)
CHANGES:
- SOLVED BUG: ver. 1.21 ayyyyyy => /aYYi/ instead of /aiiii/
- SOLVED BUG: ver. 1.21 -h won't show help unless a parameter is specified=> Now it will always show full help
- SOLVED BUG: Ver. 1.12 wronlgy transliterated 900
EOF
   exit 1; 
}

sub Number2Words {
my $eps=0.0001 ; # APPARENTLY BUG WHEN USING FLOOR OVER SOME STRINGS 
#floor((0.3+0-0)*10)=3
#floor((0.3+1-1)*10)=3
#floor((0.3+2-2)*10)=2 !!
#floor((0.3+3-3)*10)=2 !!
#floor((0.3+4-4)*10)=2 !!
#floor((0.3+5-5)*10)=2 !!
#floor((0.3+6-6)*10)=2 !!
#floor((0.3+7-7)*10)=2 !!
#floor((0.3+8-8)*10)=3
#floor((0.3+9-9)*10)=3
#floor((0.3+10-10)*10)=3
   my $N=shift;
   my $notlast=shift ;
   if ($DEBUG) {
      if ($notlast){
      print STDERR "[\nWritting Part '$N'\n" ;
      } else {
	 print STDERR "$0: Writting number $N \n"  if  $DEBUG; 
      }
   }
   my $phrase="";
   return "cero " if ($N==0);


   my $num=floor($N/1000000000000+ $eps); #/ <- Makes kate to syntax-highlight properly.
   print STDERR " $N :Conté $num bilions  [".($num>1)."] \n"  if  $DEBUG; 
   $phrase=Number2Words($num,1)." billones " if ($num>1);
   $phrase="un billón " if ($num==1);
   $N-=$num*1000000000000;
   print STDERR " Ara queda $N \n"  if  $DEBUG; 

   $num=floor($N/1000000 +$eps); #/ <- Makes kate to syntax-highlight properly.
   print STDERR " Conté $num milions  [".($num>1)."] \n"  if  $DEBUG; 
   $phrase.=Number2Words($num,1)." millones " if ($num>1);
   $phrase.="un millón" if ($num==1);

   $N-=$num*1000000;
   print STDERR " Ara queda $N \n"  if  $DEBUG;  

   $num=floor($N/1000 +$eps); #/ <- Makes kate to syntax-highlight properly.
   print STDERR " Conté $num milers  [".($num==1)."] \n"  if  $DEBUG; 
   $phrase.=Number2Words($num,1)." mil " if ($num>1);
   $phrase.="mil " if ($num==1);
   $N-=$num*1000;
   print STDERR " Ara queda $N \n"  if  $DEBUG; 

   my $numero=$N/100; #/ <- Makes kate to syntax-highlight properly.
   $num=floor($numero+$eps);
   print STDERR " Conté $num centenes  [".($num>1)."] \n"  if  $DEBUG; 

   return $phrase."cien " if ($N==100);
   $phrase.="ciento " if ($num==1);
   $phrase.="doscientos " if ($num==2);
   $phrase.="trescientos " if ($num==3);
   $phrase.="cuatrocientos " if ($num==4);
   $phrase.="quinientos " if ($num==5);
   $phrase.="seiscientos " if ($num==6);
   $phrase.="setecientos " if ($num==7);
   $phrase.="ochocientos " if ($num==8);
   $phrase.="novecientos " if ($num==9);


   my $resto=($numero-$num)*10;
   $num=floor($resto+$eps);
   print STDERR "(floor($resto)=$num, resto=$resto) Conté $num decenes   \n"  if  $DEBUG; 

   return $phrase."diez" if (abs($resto-1)<$eps);
   return $phrase."once" if (abs($resto-1.1)<$eps);
   return $phrase."doce" if (abs($resto-1.2)<$eps);
   return $phrase."trece" if (abs($resto-1.3)<$eps);
   return $phrase."catorce" if (abs($resto-1.4)<$eps);
   return $phrase."quince" if (abs($resto-1.5)<$eps);
   return $phrase.decode_utf8(encode_utf8("dieciséis")) if (abs($resto-1.6)<$eps);
   return $phrase."diecisiete" if (abs($resto-1.7)<$eps);
   return $phrase."dieciocho" if (abs($resto-1.8)<$eps);
   return $phrase."diecinueve" if (abs($resto-1.9)<$eps);
   return $phrase."veinte" if (abs($resto-2.)<$eps);
   $phrase.="veinti" if ($num==2);
   $phrase.="treinta " if ($num==3);
   $phrase.="cuarenta " if ($num==4);
   $phrase.="cincuenta " if ($num==5);
   $phrase.="sesenta " if ($num==6);
   $phrase.="setenta " if ($num==7);
   $phrase.="ochenta " if ($num==8);
   $phrase.="noventa " if ($num==9);

   $phrase.=" y " if (($num>2) && (($resto-$num)>0.09)) ;

   $resto=($resto-$num)*10;
   $num=int($resto+0.5);
   print STDERR " Conté $num unitats   \n"  if  $DEBUG; 

   $phrase.="un " if (($num==1) && ($notlast));
   $phrase.="uno " if (($num==1) && (!defined($notlast)));
   $phrase.="dos " if ($num==2);
   $phrase.="tres " if ($num==3);
   $phrase.="cuatro " if ($num==4);
   $phrase.="cinco " if ($num==5);
   $phrase.="seis " if ($num==6);
   $phrase.="siete " if ($num==7);
   $phrase.="ocho " if ($num==8);
   $phrase.="nueve " if ($num==9);
   print STDERR "ends returning '$phrase'\n]\n" if $DEBUG;
   return $phrase;
}

sub SpanishEUTRANSCRIBEPhones {
  local $_=shift ;
  chomp;
  s/x/ks/g;
  s/j/x/g;
  s/qu(?=[ie$i$e])/k/g;
  s/q/k/g;
  s/g(?=[ei$e$i])/x/g;
  s/gu(?=[ei$e$i])/g/g;
  s/(^|$V|\W)y(?=$V)/$1L/g;
  tr/y/i/;
  s/[bvw]/b/g;
  s/(?<=[aeo$aeo$i$uu])u/u/g;
  s/u(?=[aeoui$aeo$i$uu])/u/g;
  s/$u/u/g;
  s/(?<=[aeo$aeo$i$uu])i/i/g;
  s/i(?=[aeoui$aeo$i$uu])/i/g;
  s/f/f/g;
  s/ch(?=$V)/C/g;
  s/h//g;
  s/c(?=[jei$e$i])/z/g;
  tr/c/k/;
  s/rr+/R/g;
  s/L/y/g;
  s/ll/y/g;
  s/$letraenye/h/g;
  s/\W+/ /g;
  # non spanish characters:
  s/ç/s/g;
  s/S/s/g;
  # Eutranscribe conventions:
  s/C/c/g;
  s/R/\@/g;

  return ($_);
}


sub SpanishSIMPLEPhones {
  local $_=shift ;
  chomp;
  s/x/ks/g;
  s/j/x/g;
  s/qu(?=[ie$i$e])/k/g;
  s/q/k/g;
  s/g(?=[ei$e$i])/x/g;
  s/gu(?=[ei$e$i])/g/g;
  s/(^|$V|\W)y(?=$V)/$1L/g;
  tr/y/i/;
  s/[bvw]/b/g;
  s/(?<=[aeo$aeo$i$uu])u/u/g;
  s/u(?=[aeoui$aeo$i$uu])/u/g;
  s/$u/u/g;
  s/(?<=[aeo$aeo$i$uu])i/i/g;
  s/i(?=[aeoui$aeo$i$uu])/i/g;
  s/f/f/g;
  s/ch(?=$V)/C/g;
  s/h//g;
  s/c(?=[jei$e$i])/z/g;
  tr/c/k/;
  s/rr+/R/g;
  s/L/y/g;
  s/ll/y/g;
  s/$letraenye/h/g;
  s/\W+/ /g;
  # non spanish characters:
  s/ç/s/g;
  s/S/s/g;

  return ($_);
}

sub SpanishAFIPhones {
  local $_=shift ;
  chomp;
  s/x/ks/g; 
  s/j/$X/g;
  s/qu(?=[ie$i$e])/k/g;
  s/q/k/g;
  s/g(?=[ei$e$i])/$X/g;
  s/gu(?=[ei$e$i])/g/g;
  s/(^|$V|\W)y(?=$V)/$1$jdot/g;
  tr/y/j/;
  s/[bvw]/$beta/g;
  s/(?<=[aeo$aeo$i$uu])u/w/g;
  s/u(?=[aeoui$aeo$i$uu])/w/g;
  s/$u/w/g;
  s/(?<=[aeo$aeo$i$uu])i/j/g;
  s/i(?=[aeoui$aeo$i$uu])/j/g;

  s/t/$t/g;
  s/d/$d/g;
  s/f/$f/g;
  #s/$j="ʝ/g;
  s/ch(?=$V)/$tS/g;
  s/sh/$shaua/g;

  s/h//g;
  #s/$d3="ʤ/g;
  s/z/$theta/g;
  s/c(?=[jei$e$i])/$theta/g;
  tr/c/k/;
  s/d/$delta/g;
  
  #s/$zep="ʒ/g;
  #s/$s="ʂ/g;
  #s/$z="ʐ/g;
  s/d/$delta/g;
  #s/$minv="ɰ/g;
# Not useful anymore, since Syllable function returns always 'rr' when needed
#   s/(^|(?<=\s))r(?=$V)/R/g;
#   s/((?<!$V)\s+?)r(?=$V)/ R/g;
  s/rr+/R/g;
  s/r/$r/g;
  s/R/r/g;
  s/ll/$lambda/g;
  s/l/$l/g;
  #s/$l1="lʲ/g;
  #s/$m$="ɱ/g;
  #s/$n$="n̪/g;
  #s/$ndot$="n̟/g;
  #s/$n1$="nʲ/g;
  s/$letraenye/$enye/g;


  # non spanish characters:
  s/ç/s/g;
  s/S/s/g;

  return ($_);
}
