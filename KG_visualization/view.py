# from django.http import HttpResponse
from django.shortcuts import render
from py2neo import Graph
import os

# import numpy as np
# import matplotlib.pyplot as plt
# import csv
# from pandas.core.frame import DataFrame
# import pandas as pd

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username=username, password=password)


def hello(request):
    # return render(request, 'hello.html');
    return render(request, 'kg/index.html');
