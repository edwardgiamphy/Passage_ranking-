import os
from flask import Flask, request, jsonify
from rank_bm25 import BM25Okapi
import numpy as np


app = Flask(__name__)
app.secret_key = os.urandom(32)

"""Initialise"""

msmarcodata = []
with open(r"../filesndata/ms-marco-dataset/msmarco-docs.tsv", "r") as file1:
    msmarcodata=file1.readlines()
corpus_new = []

txt2docid = {}
docid2txt = {}

for entry in msmarcodata:

    entry = entry.split("\t")

    # Note: clubbing the title into the text data to form the total text data
    txt = entry[2]+' '+entry[3]  

    corpus_new.append(txt)
    txt2docid[txt] = entry[0]

# Note: here I am setting a limit due to resource constraints so that only a subset of the documents are loaded, however you may remove this limit before initialising the
# server to load the entire data
corpus_to_load = corpus_new[:5000]

tokenized_corpus = [doc.split(" ") for doc in corpus_to_load]
bm25 = BM25Okapi(tokenized_corpus)

@app.route('/bm25_query_top_n', methods=["POST"])
def bm25_query_top_n():

    json_dict = request.json
    query = json_dict['query']
    n = json_dict['n']

    tokenized_query = query.split(" ")
    ranked_passages = bm25.get_top_n(tokenized_query, corpus_to_load, n)
    ranking_ids = []
    for texts in ranked_passages:
        ranking_ids.append(txt2docid[texts])
    return jsonify(ranking_ids)

@app.route('/seektodoc', methods=["POST"])
def seektodoc():

    json_dict = request.json
    docid = json_dict['docid']

    startplace, endplace = -1, -1
    with open(r"../filesndata/ms-marco-dataset/msmarco-docs-lookup.tsv", "rt", encoding='utf8') as file1:
        for line in file1:
            line = line.rstrip().split()
            if line[0]==docid:
                startplace, endplace = int(line[2]), int(line[1])
                break
    # print(startplace, endplace)

    with open(r"../filesndata/ms-marco-dataset/msmarco-docs.tsv", "rt", encoding='utf8') as file2:
        file2.seek(int(startplace))
        json_string = file2.readline()
    
    return jsonify(json_string)

@app.route('/top100forquery', methods=["POST"])
def get_query_and_top_100_docs():

    json_dict = request.json
    query_id = json_dict['query_id']

    top100 = []
    with open(r"../filesndata/ms-marco-dataset/msmarco-doctrain-top100", "rt", encoding='utf8') as file1:
        for line in file1:
            line = line.rstrip().split()
            if line[0]==query_id:
                top100.append(line[2])

    return jsonify(top100)

@app.route('/query2queryid', methods=["POST"])
def query2queryid():

    json_dict = request.json
    query = json_dict['query']

    with open(r"../filesndata/ms-marco-dataset/msmarco-doctrain-queries.tsv", "rt", encoding='utf8') as file1:
        for line in file1:
            line = line.rstrip().split('\t', 1)
            if line[1]==query:
                return jsonify(line[0])
    
if __name__=='__main__':
    host = "localhost"
    port = 7784
    app.run(host=host, port=port, threaded=True)
