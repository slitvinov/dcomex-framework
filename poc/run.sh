: ${P=72}
for d in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/
do echo $d
done | xargs -P "$P" -I{} -n 1 sh -c \
	     'cd "{}" &&
	      date > start &&
	      dotnet ~/.local/share/DrugDeliveryModel.dll ./MSolveInput.xml 0 2>stderr 1>stdout
	      echo $? > status
	      date > end'
