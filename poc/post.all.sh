: ${zip=B.zip}
rm $zip

m=0
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then m=$((m+1))
	zip -qr9 "$zip" ${d} || exit 1
   fi
done
echo $m "$zip"
