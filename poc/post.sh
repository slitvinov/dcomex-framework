: ${zip=b.zip}
rm $zip

m=0 n=
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test -f ${d}status
   then r=`cat ${d}status`
	m=$((m+1))
	case $r in
	    0) ;;
	    *) n=$((n+1))
	       zip -qr9 "$zip" ${d}MSolveInput.xml
	       zip -qr9 "$zip" ${d}stderr ;;
	esac
   fi
done
echo $n/$m "$zip"
