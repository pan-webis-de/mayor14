python src/authorid_sparse.py -m devel --percentage .6 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_60.txt

python src/authorid_sparse.py -m devel --percentage .7 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_70.txt

python src/authorid_sparse.py -m devel --percentage .8 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_80.txt

python src/authorid_sparse.py -m devel --percentage .9 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_90.txt

python src/authorid_sparse.py -m devel --percentage .95 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_95.txt

python src/authorid_sparse.py -m devel --percentage .98 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_percentage_98.txt



python src/authorid_sparse.py -m devel --documents 4 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_documents_4.txt

python src/authorid_sparse.py -m devel --documents 5 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_documents_5.txt

python src/authorid_sparse.py -m devel --documents 6 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_documents_6.txt

python src/authorid_sparse.py -m devel --imposters 10 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_imposters_10.txt

python src/authorid_sparse.py -m devel --imposters 15 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_imposters_15.txt

python src/authorid_sparse.py -m devel --imposters 5 data/PAN14 data/PAN14/truth.txt > data/PAN14/answers_sparse.txt
python src/eval_pan.py data/PAN14/truth.txt data/PAN14/answers_sparse.txt > eval_imposters_5.txt


