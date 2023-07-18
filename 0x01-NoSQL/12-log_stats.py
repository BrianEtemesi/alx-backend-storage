#!/usr/bin/env python3
"""
script to provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
	client = MongoClient()
	nginx_collection = client.logs.nginx
    c_len = len(list(nginx_collection.find()))
    print(c_len, "logs\nMethods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        print(
            "\tmethod {}: {}".format(
                method, len(list(nginx_collection.find({"method": method})))
                )
            )
    print(
        "{} status check".format(
            len(list(
                nginx_collection.find({"method": "GET", "path": "/status"})
                ))
            )
        )
