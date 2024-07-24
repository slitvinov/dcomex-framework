for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do t=${d}tumorVolume_AnalysisNo_0.txt
   e=${d}stderr
   if test -f $t
   then
       n=`awk '{ for (i = 1; i <= NF; i++) if ($i == 0) {print i; exit} }' $t`
       if test -s $e
       then echo $d `test -s $e && echo 1`
	    zip -qr9 f.zip ${d}MSolveInput.xml || exit 1
	    zip -qr9 f.zip ${d}stderr || exit 1
       fi
   fi
done
