#!/usr/bin/env python3
"""
defines a pymongo function
"""


def schools_by_topic(mongo_collection, topic):
	"""
	returns a list of schools having a specific topic
	"""
	return mongo_collection.find({'topics': topic})
