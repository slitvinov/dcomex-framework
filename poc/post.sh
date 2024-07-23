for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do t=${d}tumorVolume_AnalysisNo_0.txt
   e=${d}stderr
   if test -f $t
   then
       n=`awk '{ for (i = 1; i <= NF; i++) if ($i == 0) {print i; exit} }' ${d}tumorVolume_AnalysisNo_0.txt`
       if test $n -eq 990 -o -s $e
       then echo $d `test -s $e && echo 1`
	    zip -qr9 A.zip $d || exit 1
       fi
   fi
done
