: ${zip=B.zip}
rm $zip

m=0
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then m=$((m+1))
	       zip -qr9 "$zip" \
${d}Ag_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}AgIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}APC_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}APCIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}aPDL1_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}aPDL1Iterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}c_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}cIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}cox_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}coxIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}end \
${d}IAPC_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}IAPCIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}In_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}InIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}lamda_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}lamdaIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}MSolveInput.xml \
${d}parameters_AnalysisNo_1.txt \
${d}porousIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}prescribedTimeSteppingList.txt \
${d}staggeredIterations_AnalysisNo_1.txt \
${d}start \
${d}status \
${d}stderr \
${d}stdout \
${d}t_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}TE_AnalysisNo_1_solutionData_AnalysisNo_1.txt \
${d}TEIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}timeStepTotalTimes_AnalysisNo_1.txt \
${d}tIterations_AnalysisNo_1_iterations_AnalysisNo_1.txt \
${d}tumorVolume_AnalysisNo_1.txt \

   fi
done
echo $m "$zip"
