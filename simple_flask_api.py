# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 17:28:10 2021

@author: Michael Gorbatenko
"""
import pandas as pd 
import numpy as np 
import os 
import json 
import flask
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine, text

# Create flask app instance
app = Flask(__name__)

# create api instance 
api = Api(app) 


def pandas_load_data():
    df = pd.read_json("data/zillow_data.json", orient="split")
    return df

def load_data():
    with open("data/zillow_data.json", "r") as f:
        data = json.load(f)
    return data

def parse_dict_by_metric(_dict, var):
    data = [item for item in _dict['data'] if item[0] == var]
    return data
    

class Inventory(Resource):
    
    def __init__(self):
        self.columns = ["Metric",
                         "RegionID",
                         "SizeRank",
                         "RegionName",
                         "RegionType",
                         "StateName",
                         "Week",
                         "value"]
        self.column_name = "For-Sale Inventory Count"
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('StateName', type = str, default = None)
        self.parser.add_argument('SizeRank', type = int, default = None)
        self.parser.add_argument('RegionName', type = str, default = None)
        self.args = self.parser.parse_args()
        
        
    def get(self):
        data = load_data()
        data = parse_dict_by_metric(data, self.column_name)
        for arg, value in self.args.items():
            if value:
                data = self.find_by_filter(data, arg)
        return flask.jsonify(data)
    
    def find_by_filter(self, data, column):
        idx = self.columns.index(column)
        data = [item for item in data if item[idx]==self.args[column]]
        return data
    

class SalePrice(Resource):

    def __init__(self):
        self.columns = ["Metric",
                         "RegionID",
                         "SizeRank",
                         "RegionName",
                         "RegionType",
                         "StateName",
                         "Week",
                         "value"]
        self.column_name = "Median Sale Price"
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('StateName', type = str, default = None)
        self.parser.add_argument('SizeRank', type = int, default = None)
        self.parser.add_argument('RegionName', type = str, default = None)
        self.args = self.parser.parse_args()
        
        
    def get(self):
        data = load_data()
        data = parse_dict_by_metric(data, self.column_name)
        for arg, value in self.args.items():
            if value:
                data = self.find_by_filter(data, arg)
        return flask.jsonify(data)
    
    def find_by_filter(self, data, column):
        idx = self.columns.index(column)
        data = [item for item in data if item[idx]==self.args[column]]
        return data
    
    
api.add_resource(Inventory, '/inventory')
api.add_resource(SalePrice, '/saleprice')

if __name__ == "__main__":
    app.run(port=5555)