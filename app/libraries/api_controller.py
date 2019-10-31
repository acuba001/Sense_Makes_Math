import requests

class controller:
	def __init__(self, type, method, params):
		self.type = type
		self.method = method
		self.params = params
