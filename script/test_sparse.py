

for rep in capital punct letters comma enter wordpar sntcpar
do
    python src/authorid_sparse.py -m devel --documents 4 -r ${rep} -r bigrampref  data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_documents_4${rep}.txt

    python src/authorid_sparse.py -m devel --documents 5 -r ${rep} -r bigrampref data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_documents_5${rep}.txt

    python src/authorid_sparse.py -m devel --documents 6 -r ${rep} -r bigrampref data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_documents_6${rep}.txt

    python src/authorid_sparse.py -m devel --imposters 10 -r ${rep} -r bigrampref data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_imposters_10${rep}.txt

    python src/authorid_sparse.py -m devel --imposters 15 -r ${rep} -r bigrampref data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_imposters_15${rep}.txt

    python src/authorid_sparse.py -m devel --imposters 5 -r ${rep} -r bigrampref data/pan14_train data/pan14_train/truth.txt > data/pan14_train/answers_sparse.txt
    python src/eval_pan.py data/pan14_train/truth.txt data/pan14_train/answers_sparse.txt > eval_imposters_5${rep}.txt
done

