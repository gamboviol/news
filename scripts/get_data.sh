#/bin/bash

RCV1=http://jmlr.csail.mit.edu/papers/volume5/lewis04a

set -e

echo "[*] get RCV1-v2 dataset"
echo "[*] see $RCV1/lyrl2004_rcv1v2_README.htm for details"

echo "[*] making data dir"
mkdir -p rcv1

echo "[*] downloading files..."
wget $RCV1/a08-topic-qrels/rcv1-v2.topics.qrels.gz -O rcv1/topics.gz
wget $RCV1/a11-smart-stop-list/english.stop -O rcv1/stopwords
wget $RCV1/a14-term-dictionary/stem.termid.idf.map.txt -O rcv1/token_id_idf
wget $RCV1/a12-token-files/lyrl2004_tokens_train.dat.gz -O rcv1/tokens_train.gz
for i in 0 1 2 3; do
  wget $RCV1/a12-token-files/lyrl2004_tokens_test_pt$i.dat.gz -O rcv1/tokens_test$i.gz
done

echo "[*] decompressing files..."
gunzip rcv1/topics.gz rcv1/tokens_*.gz

echo "[*] combining and converting token files..."
cat rcv1/tokens_* > rcv1/tokens.smart
python scripts/smart2low.py rcv1/tokens.smart rcv1/tokens
rm rcv1/tokens_* rcv1/tokens.smart

echo "[*] done!"
