
# This file is mainly for doing random tests before adding the functionalities to the main_code.py file

from clocq.interface.CLOCQInterfaceClient import CLOCQInterfaceClient
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

clocq = CLOCQInterfaceClient(host="http://localhost", port="7778")

def make_graph_from_entities2(kb_indexes):

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

def clean_list_and_remove_redundant2(kb_indexes_lists, check_against=[]):
	labels_list=[]
	for kb_index_list in kb_indexes_lists:
		for kb_index in kb_index_list:
			label = clocq.get_label(kb_index)
			if (label!=kb_index) and (kb_index not in check_against):
				labels_list.append(kb_index)
	labels_list = list(set(labels_list))
	return labels_list

def networkx_draw_graph(all_nodes, subgraph, savepath, figsize=(200, 80), dpi=80):
	labels = {}
	for node in all_nodes:
		if node not in labels:
			labels[node] = clocq.get_label(node)

	fig = plt.figure(1, figsize, dpi)
	g = nx.DiGraph(subgraph)
	h = nx.relabel_nodes(g, labels)
	nx.draw_networkx(h, with_labels=True, font_size=8)
	plt.savefig(savepath, format="PNG")

# using some randomly obtained results here to test the code:
z = [['Q362', 'Q127050', 'Q8789', 'Q2915210', 'Q7516763', 'Q362', 'Q213302', 'Q937', 'Q127050', 'Q127050', 'Q127050', 'Q362', 'Q46', 'Q127050', 'Q183', 'Q5338648', 'Q172948', 'Q11429', 'Q6927', 'Q7325', 'Q183', 'Q127050', 'Q12802', 'Q127050', 'Q7144004', 'Q362', 'Q590490', 'Q7968612', 'Q12802'], ['Q5364403', 'Q5364404', 'Q80042', 'Q193891'], ['Q7201367', 'Q7201388', 'Q7571373', 'Q6989459', 'Q2091008', 'Q7571373', 'Q485446', 'Q865588'], ['Q39681', 'Q7767051', 'Q7388880', 'Q7770682', 'Q7832844', 'Q785373', 'Q58024', 'Q785373', 'Q11759562', 'Q11148', 'Q16', 'Q145', 'Q30', 'Q105973', 'Q2016165', 'Q215279', 'Q973587', 'Q22905934', 'Q141090', 'Q2935914', 'Q4917', 'Q2450848', 'Q2935914', 'Q9158', 'Q9158', 'Q483959', 'Q39681', 'Q7767051', 'Q1050775', 'Q1477856', 'Q3972943', 'Q7628158', 'Q1142825', 'Q2935914', 'Q11759562', 'Q2935914', 'Q11759562', 'Q35127', 'Q130', 'Q18154638', 'Q105973', 'Q4116214', 'Q7318025', 'Q483959', 'Q75', 'Q18154638', 'Q483959', 'Q1070699', 'Q105973', 'Q18154638', 'Q30', 'Q1335296', 'Q11307668', 'Q11307668', 'Q263187', 'Q4833730', 'Q6805535', 'Q18154638', 'Q674950', 'Q7810144', 'Q27318', 'Q9158', 'Q18154638', 'Q7810144', 'Q215279', 'Q8091', 'Q16834870', 'Q37437', 'Q9158', 'Q7810144', 'Q5614028', 'Q13961', 'Q5635494', 'Q196066', 'Q18154638', 'Q16834870', 'Q3307269', 'Q29485', 'Q5164835', 'Q24963804', 'Q13961', 'Q7810144', 'Q9158', 'Q3208168', 'Q16834870', 'Q18154638', 'Q29485', 'Q215279', 'Q5532547', 'Q9158', 'Q27318', 'Q170420', 'Q29485', 'Q215279', 'Q7265505', 'Q9158', 'Q7810144', 'Q27318', 'Q18154638', 'Q675059', 'Q2920921', 'Q658715', 'Q215279', 'Q2367247', 'Q11759562', 'Q7759071', 'Q11759562', 'Q16834870', 'Q16834870', 'Q35127', 'Q39681', 'Q7767051', 'Q5377930', 'Q30849', 'Q16834870', 'Q18154638', 'Q7318025', 'Q7833912', 'Q17142652', 'Q18154638'], ['Q7309424', 'Q189004', 'Q1259650', 'Q1335296', 'Q865588', 'Q329777', 'Q2269240', 'Q7333711', 'Q2250054', 'Q17056648'], ['Q1858336', 'Q130283', 'Q216774', 'Q1350935', 'Q130283', 'Q4916880', 'Q68340', 'Q15698345', 'Q68340', 'Q244403', 'Q4916880', 'Q692', 'Q6555571', 'Q130283', 'Q92611', 'Q9476', 'Q130283', 'Q130283', 'Q130283', 'Q692', 'Q130283', 'Q2454065', 'Q692', 'Q692', 'Q1028188', 'Q130283', 'Q1553339', 'Q1026782', 'Q259745', 'Q1028188', 'Q130283', 'Q130283', 'Q214267', 'Q130283', 'Q1026782', 'Q21932179', 'Q130283', 'Q15698345', 'Q2724880', 'Q2454065', 'Q130283', 'Q564', 'Q130283', 'Q130283', 'Q7729816', 'Q193543', 'Q2454065', 'Q15698348', 'Q15698348', 'Q130283', 'Q2454065', 'Q259745', 'Q2454065', 'Q15698348', 'Q3429667', 'Q130283', 'Q130283', 'Q2308809', 'Q259745', 'Q2308809'], ['Q8068', 'Q8068', 'Q8068', 'Q8068', 'Q8068', 'Q8068', 'Q36074', 'Q36074', 'Q3112627', 'Q2986415', 'Q4917', 'Q47041', 'Q170321', 'Q8068', 'Q43183', 'Q37813', 'Q8068', 'Q161598', 'Q49389', 'Q702492', 'Q4022', 'Q43619', 'Q8068', 'Q140075', 'Q36074', 'Q4611820', 'Q5133416', 'Q7597575', 'Q5381330', 'Q408', 'Q657157', 'Q643249', 'Q121359'], ['Q263886', 'Q264238', 'Q644302', 'Q445235', 'Q6097', 'Q8486', 'Q1910318', 'Q644302', 'Q15982858', 'Q795052', 'Q364340', 'Q327245'], ['Q154510', 'Q22890', 'Q7156780', 'Q8062', 'Q12638', 'Q8062', 'Q6071404', 'Q22890', 'Q12638', 'Q6071406', 'Q6071403', 'Q490513', 'Q490513', 'Q140845', 'Q22890', 'Q131257', 'Q17087058', 'Q22890', 'Q22890', 'Q182722'], ['Q82059', 'Q1544247', 'Q82059', 'Q1544247', 'Q7915723', 'Q325421', 'Q10851960', 'Q7915723', 'Q918', 'Q658255', 'Q10851960', 'Q219577', 'Q75', 'Q325421', 'Q16988318', 'Q17042822', 'Q6763754', 'Q5090400', 'Q5013652', 'Q7596586', 'Q25344976', 'Q16988318', 'Q5087180', 'Q4806263', 'Q7554233', 'Q16734888', 'Q1544247', 'Q17068426', 'Q956', 'Q9158', 'Q1444179', 'Q11035', 'Q148']]
query_ent = ['Q127050']

all_entities = clean_list_and_remove_redundant2(z, query_ent)

print(all_entities)

subgraph = {}
all_nodes = []

def flatten_path_and_make_graph1(path):
	for listitem in path:
		if type(listitem[0])==str:
			sub = listitem[0]
			all_nodes.append(sub)
			if sub not in subgraph:
				subgraph[sub] = []
			for i in range(1, len(listitem),2):
				pred,ob = listitem[i], listitem[i+1]
				if ob[0] not in ["P", "Q"]:
					continue
				subgraph[sub].append(ob)
				all_nodes.append(ob)
		else:
			flatten_path_and_make_graph1(listitem)

for qent in query_ent:
	for docent in all_entities:
		res = clocq.connectivity_check(qent, docent)
		if res==1:
			print(qent, docent, res)
			path = clocq.connect(qent, docent)
			flatten_path_and_make_graph1(path)

# check connectivity among entities even if from same document
for i in range(len(all_entities)):
	for j in range(i+1, len(all_entities)):
		ent1 = all_entities[i]
		ent2 = all_entities[j]
		res = clocq.connectivity_check(ent1, ent2)
		if res==1:
			path = clocq.connect(ent1, ent2)
			print(ent1, ent2)
			flatten_path_and_make_graph1(path)

all_nodes = list(set(all_nodes))
for k in subgraph:
	subgraph[k] = list(set(subgraph[k]))
print(subgraph)
networkx_draw_graph(all_nodes=all_nodes, subgraph=subgraph, savepath=r'graph_sample.png', dpi=80, figsize=(100, 40))

# # check connectivities between different doc entities
# for i in range(len(z)):
# 	list1 = z[i]
# 	for j in range(i+1, len(z)):
# 		list2 = z[j]
# 		for ent1 in list1:
# 			for ent2 in list2:
# 				res = clocq.connectivity_check(ent1, ent2)
# 				if res==1:
# 					print(clocq.get_label(ent1), clocq.get_label(ent2), res)

# def make_graph(path, subgraph = {}, all_nodes = []):
# 	subgraph = {}
# 	all_nodes = []
# 	def flatten_path_and_make_graph1(path):
# 		for listitem in path:
# 			if type(listitem[0])==str:
# 				sub = listitem[0]
# 				all_nodes.append(sub)
# 				if sub not in subgraph:
# 					subgraph[sub] = []
# 				for i in range(1, len(listitem),2):
# 					pred,ob = listitem[i], listitem[i+1]
# 					if ob[0] not in ["P", "Q"]:
# 						continue
# 					subgraph[sub].append(ob)
# 					all_nodes.append(ob)
# 			else:
# 				flatten_path_and_make_graph1(listitem)
# 	flatten_path_and_make_graph1(path)
# 	all_nodes = list(set(all_nodes))
# 	return subgraph, all_nodes

# ent1 = 'Q384238'
# ent2 = 'Q4916880'
# path = clocq.connect(ent1, ent2)
# print(path)
# subgraph, all_nodes = make_graph(path)
# print(subgraph, all_nodes)
# networkx_draw_graph(all_nodes=all_nodes, subgraph=subgraph, savepath=r'graph_sample.png')
