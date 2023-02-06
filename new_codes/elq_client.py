import json
import requests

class ELQ_ClientInterface:
	def __init__(self, host="http://localhost", port="7780"):
		self.host = host
		self.port = port
		self.req = requests.Session()
	
	def get_entities(self, text_for_elq, numberoftokenspersentence):
		params = {"text": text_for_elq, "numberoftokenspersentence": numberoftokenspersentence}
		res = self._req("/get_entities", params)
		json_string = res.content.decode("utf-8")
		res = json.loads(json_string)
		return res
	
	def _req(self, action, json):
		return self.req.post(self.host + ":" + str(self.port) + action, json=json)

if __name__ == "__main__":
	elq = ELQ_ClientInterface(port="7780")
