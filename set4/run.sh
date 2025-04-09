for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do if test ! -f $d/status
   then echo $d
   fi
done | xargs --process-slot-var I -P `nproc` -n 1 sh -xuc \
	     '
trap "exit 1" 1 2 15
cd "$0" &&
    date > start &&
    taskset --cpu-list $I \
	    dotnet ~/.local/share/DrugDeliveryModel.dll ./MSolveInput.xml 0 \
	    2>stderr 1>stdout
echo $? > status
date > end
'
