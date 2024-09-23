: ${P=64}
n=1024
i=0
while :
do if test $i -eq $n; then break; fi
   d=`printf %08d $i`
   echo $d
   i=$((i+1))
done | xargs -P "$P" -I{} -n 1 sh -c \
	     'cd "{}" &&
	      date > start &&
	      dotnet ~/.local/share/DrugDeliveryModel.dll ./MSolveInput.xml 0 2>stderr 1>stdout
	      echo $? > status
	      data > end'
