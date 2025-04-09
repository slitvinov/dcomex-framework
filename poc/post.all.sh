set -eu

: ${zip=B.zip}
rm -f $zip
m=0
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then m=$((m+1))
	zip -qr9 "$zip" \
	    ${d}* \
	    --exclude \
	    ${d}APC_mslv_1.txt \
	    ${d}APC_mslv_2.txt \
	    ${d}APC_mslv_3.txt \
	    ${d}APC_mslv_4.txt \
	    ${d}APC_mslv_5.txt \
	    ${d}c_mslv_1.txt \
	    ${d}c_mslv_2.txt \
	    ${d}c_mslv_3.txt \
	    ${d}c_mslv_4.txt \
	    ${d}c_mslv_5.txt \
	    ${d}cox_msolve_1.txt \
	    ${d}cox_msolve_2.txt \
	    ${d}cox_msolve_3.txt \
	    ${d}cox_msolve_4.txt \
	    ${d}cox_msolve_5.txt \
	    ${d}TE_mslv_1.txt \
	    ${d}TE_mslv_2.txt \
	    ${d}TE_mslv_3.txt \
	    ${d}TE_mslv_4.txt \
	    ${d}TE_mslv_5.txt \

	    echo $m >&2
   fi
done
echo $m "$zip"
