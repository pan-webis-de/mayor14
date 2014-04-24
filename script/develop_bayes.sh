#para probrar: bash script/develop_bayes.sh data/pan14-train data/pan14-train

if [ $# -lt 2 ]
then
	echo "Usage: `basename $0` InputDirectory OutputDirectory"
	echo "For extra options look at authorid.py script or README file"
	exit 1
fi

python src/authorid_bayes.py ${@:1:$len} ${@: -2} > ${@: -1}/final_bayes.txt
echo "Saving results to" ${@: -1}/final_bayes.txt     
python src/eval_pan.py data/pan14-train/truth.txt data/pan14-train/final_bayes.txt > ${@: -1}/eval_final.txt

