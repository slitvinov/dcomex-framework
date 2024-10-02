: ${tar=~/1.tar}
m=0
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then m=$((m+1))
	tar -rf "$tar" \
	    ${d}MSolveInput.xml \
	    ${d}prescribedTimeSteppingList.txt \
	    ${d}status \
	    ${d}stderr \
	    ${d}timeStepTotalTimes_AnalysisNo_1.txt \
	    ${d}tumorVolume_AnalysisNo_1.txt \
	    || exit 1
   fi
done
gzip -f9 "$tar"
