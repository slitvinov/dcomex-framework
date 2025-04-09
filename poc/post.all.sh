: ${zip=B.zip}
rm $zip

m=0
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then m=$((m+1))
	zip -qr9 "$zip" \
	    ${d}* \
	    --exclude \
	    cox_msolve_1.txt \
	    cox_msolve_2.txt \
	    cox_msolve_3.txt \
	    cox_msolve_4.txt \
	    cox_msolve_5.txt \
	    APC_mslv_1.txt \
	    APC_mslv_2.txt \
	    APC_mslv_3.txt \
	    APC_mslv_4.txt \
	    APC_mslv_5.txt \
	    c_mslv_1.txt \
	    c_mslv_2.txt \
	    c_mslv_3.txt \
	    c_mslv_4.txt \
	    c_mslv_5.txt \
	    TE_mslv_1.txt \
	    TE_mslv_2.txt \
	    TE_mslv_3.txt \
	    TE_mslv_4.txt \
	    TE_mslv_5.txt || break
   fi
done
echo $m "$zip"
