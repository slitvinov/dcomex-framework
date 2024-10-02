: ${tar=~/1.tar}
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
      tar -rf "$tar" \
	  ${d}MSolveInput.xml \
	  ${d}status \
	  ${d}timeStepTotalTimes_AnalysisNo_1.txt \
	  ${d}tumorVolume_AnalysisNo_1.txt \
	  || exit 1
   fi
done
# gzip -f9 "$tar"
