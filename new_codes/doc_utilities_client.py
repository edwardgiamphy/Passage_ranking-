import json
import requests
from elq_client import ELQ_ClientInterface
import time

class DocUtilityInterface:
	def __init__(self, host="http://localhost", port="7784"):
		self.host = host
		self.port = port
		self.req = requests.Session()
	
	def bm25_query_top_n(self, query, n):
		params = {"query": query, "n": n}
		res = self._req("/bm25_query_top_n", params)
		json_string = res.content.decode("utf-8")
		res = json.loads(json_string)
		return res
	
	def seektodoc(self, docid):
		params = {"docid": docid}
		res = self._req("/seektodoc", params)
		json_string = res.content.decode("utf-8")
		res = json.loads(json_string)
		return res
	
	def get_query_and_top_100_docs(self, query_id):
		params = {"query_id": query_id}
		res = self._req("/top100forquery", params)
		json_string = res.content.decode("utf-8")
		res = json.loads(json_string)
		return res
	
	def query2queryid(self, query):
		params = {"query": query}
		res = self._req("/query2queryid", params)
		json_string = res.content.decode("utf-8")
		res = json.loads(json_string)
		return 'D'+res
	
	def _req(self, action, json):
		return self.req.post(self.host + ":" + str(self.port) + action, json=json)

if __name__ == "__main__":
	
	dut = DocUtilityInterface(port="7784")
