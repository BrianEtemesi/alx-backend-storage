#!/usr/bin/env python3
"""
defines a pymongo function
"""
from pymongo import MongoClient


def list_all(mongo_collection):
	"""
	returns a list of all documents in a collection
	"""
	
	my_list = []
	for i in mongo_collection.find():
		my_list.append(i)
	return my_list
	 
