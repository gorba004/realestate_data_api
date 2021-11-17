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
        self.column_name = "For-Sale Inventory Count"
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('StateName', type = str, default = None)
        self.parser.add_argument('SizeRank', type = int, default = None)
        self.args = self.parser.parse_args()
        print(self.args)
        
        
    def get(self):
        data = load_data()
        data = parse_dict_by_metric(data, self.column_name)
        if self.args['StateName']:
            data = self.find_by_state(data)
        if self.args['SizeRank']:
            data = self.find_by_rank(data)          
        return flask.jsonify(data)
    
    def find_by_state(self, data):
        data = [item for item in data if item[5]==self.args['StateName']]
        return data
    
    def find_by_rank(self, data):
        data = [item for item in data if item[2]==self.args['SizeRank']]
        return data

class SalePrice(Resource):

    def __init__(self):
        self.column_name = "Median Sale Price"
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('StateName', type = str, default = None)
        self.parser.add_argument('SizeRank', type = int, default = None)
        self.args = self.parser.parse_args()
        print(self.args)
        
        
    def get(self):
        data = load_data()
        data = parse_dict_by_metric(data, self.column_name)
        if self.args['StateName']:
            data = self.find_by_state(data)
        if self.args['SizeRank']:
            data = self.find_by_rank(data)          
        return flask.jsonify(data)
    
    def find_by_state(self, data):
        data = [item for item in data if item[5]==self.args['StateName']]
        return data
    
    def find_by_rank(self, data):
        data = [item for item in data if item[2]==self.args['SizeRank']]
        return data
    
    
api.add_resource(Inventory, '/inventory')
api.add_resource(SalePrice, '/saleprice')

if __name__ == "__main__":
    app.run(port=5555)