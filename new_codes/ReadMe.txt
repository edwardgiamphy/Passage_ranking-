
You will require the following first:
    https://github.com/PhilippChr/CLOCQ
    https://github.com/facebookresearch/BLINK

MSmarco dataset can be found at:
    https://microsoft.github.io/msmarco/TREC-Deep-Learning-2019.html
download the files under Document Ranking dataset

Place the elq_server.py file in BLINK/ 

Please set the ports carefully before running the server files to initialise the servers.
Initialise the 3 flask servers:
    elq_server.py
    doc_utilities_server.py
    CLOCQInterfaceServer.py
And then use the other code files that will make calls to these servers running on localhost.
The 3 servers currently take around 500 GB of memory space, so make sure you have enough space before running.
Apparently, CLOCQ takes around 370 GB and the space by doc_utilities_server.py can be reduced by:
        editing the line 'corpus_to_load = corpus_new[:5000]'. The 5000 limit loads only the 5000 documents from MS Marco dataset. 
        Remove this limit to load the entire dataset.

Note that the file structure is quite messy because I am still working on most of the code. Apologies for that.
For Example, I stored the MSmarco dataset in the 'filesndata/ms-marco-dataset' folder in the root directory
It would be better if you can keep the same naming convention, else change the paths in all the codes.

