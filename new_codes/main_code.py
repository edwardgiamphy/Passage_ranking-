from clocq import config
from clocq.interface.CLOCQInterfaceClient import CLOCQInterfaceClient
from elq_client import ELQ_ClientInterface
import networkx as nx
import matplotlib.pyplot as plt
import time
from doc_utilities_client import DocUtilityInterface
import json

def clean_list_and_remove_redundant(kb_indexes):
	labels_list=[]
	for kb_index in kb_indexes:
		label = clocq.get_label(kb_index)
		if label!=kb_index:
			labels_list.append(kb_index)
	labels_list = list(set(labels_list))
	return labels_list

def make_graph_from_entities(kb_indexes):

	subgraph = {}
	all_nodes = []
	# format of an entry in subgraph = {subject: [<object, relation>]}
	
	for kb_index in kb_indexes:
		all_nodes.append(kb_index)
		neighbours = clocq.get_neighborhood(kb_index, p=100)
		for entry in neighbours:
			sub = entry[0]
			if sub['id'] not in subgraph:
				subgraph[sub['id']] = []
			for i in range(1, len(entry),2):
				pred,ob = entry[i], entry[i+1]
				if ob['id'][0] not in ["P", "Q"]:
					continue
				subgraph[sub['id']].append(ob['id'])
				all_nodes.append(ob['id'])
	all_nodes = list(set(all_nodes))
	return subgraph, all_nodes

def networkx_draw_graph(all_nodes, subgraph, savepath):
	labels = {}
	for node in all_nodes:
		if node not in labels:
			labels[node] = clocq.get_label(node)

	fig = plt.figure(1, figsize=(200, 80), dpi=80)
	g = nx.DiGraph(subgraph)
	h = nx.relabel_nodes(g, labels)
	nx.draw_networkx(h, with_labels=True, font_size=8)
	plt.savefig(savepath, format="PNG")

if __name__=='__main__':

	# at multiple places here I have used time functions to find the code runtime, you may hide those lines if you want
	dut = DocUtilityInterface(port="7784")
	elq = ELQ_ClientInterface(port="7780")
	clocq = CLOCQInterfaceClient(host="http://localhost", port="7778")
	
	query = ")what was the immediate impact of the success of the manhattan project?"
	query_id = dut.query2queryid(query=query)

	starttime = time.perf_counter()
	top_res = dut.bm25_query_top_n(query=query, n=10)
	endtime = time.perf_counter()
	print("time taken to obtain top n docs from corpus:", endtime-starttime)

	all_entities_from_data = []

	starttime = time.perf_counter()

	# since we need the entities from the question query too, and keeping the number of tokens (words) per sentence low around 5 because the query
	# will probably be a short sentence. Try for other values too.
	entities_from_query = elq.get_entities(text_for_elq=query, numberoftokenspersentence=5)

	with open(r"../BLINK/models/id2wikidata.json", "r") as jsonfile1:
		json_data = json.load(jsonfile1)
			
	for docid in top_res:
		text = dut.seektodoc(docid=docid)
		text = text.split("\t")
		query = text[2]+' '+text[3] 
		entities_obtained = elq.get_entities(text_for_elq=query, numberoftokenspersentence=350)
		all_entities_from_data.append(entities_obtained)

	endtime = time.perf_counter()
	print("time taken to obtain entities:", endtime-starttime)
	print("length of entities list", all_entities_from_data)

	# print(entities_from_query, all_entities_from_data)

	
	
