: ${P=72}
for i in */*/MSolveInput.xml
do dirname $i
done | xargs -P "$P" -I{} -n 1 sh -c \
	     'cd "{}" &&
	      date > start &&
	      dotnet ~/.local/share/DrugDeliveryModel.dll ./MSolveInput.xml 0 2>stderr 1>stdout
	      echo $? > status
	      date > end'
