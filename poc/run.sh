n=1024
i=0
while :
do if test $i -eq $n; then break; fi
   d=`printf %08d $i`
   echo $d
   i=$((i+1))
done | xargs -P 64 -I{} -n 1 sh -c 'cd "{}" && dotnet ~/.local/share/MGroup.MSolve4Korali.dll MSolveInput.xml 0 2>stderr 1>stdout; echo $? > status'
