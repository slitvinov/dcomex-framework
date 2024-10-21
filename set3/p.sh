ssh grace 'rm -f 3.tar.gz 3.tar'

for h in grace grace2
do ssh $h '
cd /scratch/slitvinov/set3 &&
tar=~/3.tar sh /scratch/slitvinov/dcomex-framework/poc/post.tumor.sh
'
done

ssh grace 'gzip -9 -f ~/3.tar'
scp grace:3.tar.gz .
