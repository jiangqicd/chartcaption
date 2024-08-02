#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File:app.py
@description:
@Time:2023/12/20 8:13:01
@Author:jiangqi
@Email:jiangqi@zjut.edu.cn
'''


import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from pandas.api.types import is_numeric_dtype
import copy
from utils.condition import time_keywords
from utils.selectedChart import selectedChart
from annotationGenerator import annotationGenerator

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
csv_name = ""


@app.route('/test', methods=['POST', 'GET'])
def test():
    return jsonify({"可以正确访问": "it is ok!"})


@app.route('/get-table-csv', methods=['POST'])
def get_csv():
    data = request.json
    print(data)
    csv_name = data.get('selected_table').get('_value')
    print(csv_name)
    csv_path = os.path.dirname(__file__)+"/data/"+csv_name  # 指定 CSV 文件路径
    print(os.path.dirname(__file__))
    if os.path.exists(csv_path):

        table = pd.read_csv(csv_path)

        # map_attr_type存储了表格数据中属性的类别，例如"Year": "temporal"
        map_attr_type = {}

        for attr in table.columns:
            if any(s.lower() in attr.lower() for s in time_keywords):
                map_attr_type[attr] = "temporal"
            if attr not in map_attr_type:
                if is_numeric_dtype(table[attr]):
                    map_attr_type[attr] = "numerical"
                else:
                    map_attr_type[attr] = "categorical"

        # selectedchart为当前关注的图表
        selectedchart = selectedChart(csv_name, table, map_attr_type).chart
        ts = dataprocessing(table, selectedchart)
        result = {"map_attr_type": map_attr_type,
                  "tableRecords": table.to_json(orient='records'),
                  "selectedChart": selectedchart,
                  "ts": ts}

        # print(selectedchart)
        return jsonify(result)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/get-pattern-annotation', methods=['POST'])
def get_pattern_annotation():
    # 获取请求中的JSON数据
    data = request.get_json()

    csv_name = data.get('selectedTable')
    print(csv_name)

    if csv_name == "vaccine_correlation.csv":
        selectedChart = data.get('selectedChart')
        with open(selectedChart["y"]["name"]+'.json', 'r', encoding='utf-8') as file:
            selectedChart = json.load(file)
    else:
        csv_path = os.path.dirname(__file__)+"/data/"+csv_name
        table = pd.read_csv(csv_path)

        selectedChart = data.get('selectedChart')
        print("----------------")
        # print(selectedChart)

        d = copy.deepcopy(selectedChart)

        for key, value in d.items():
            # 检查当前项是否为字典，确保我们处于第一层
            if key == "table":
                # 尝试从第二层删除指定的key
                del value["data"]
        print(d)

        annotator = annotationGenerator(table, selectedChart)
        annotator.generate()
        selectedChart = annotator.chart
        with open(selectedChart["y"]["name"]+'.json', 'w', encoding='utf-8') as file:
            json.dump(selectedChart, file, indent=4)
            # selectedChart = json.load(file)
    # for i in annotator.numerical_attr_data.keys():
    #     print(i)
    #     print(annotator.numerical_attr_data[i])
    # print(annotator.annotations)
    # print(annotator.line_patterns_with_annotations)
    res = {"annotatedChart": selectedChart}
    return jsonify(res)


def dataprocessing(Table, selectedchart):
    # print(list(table[selectedchart["x"]["name"]]))
    table = Table.copy(deep=True)
    table[selectedchart["x"]["name"]
          ] = table[selectedchart["x"]["name"]].astype(str)
    table["processed_time_column"] = pd.to_datetime(
        table[selectedchart["x"]["name"]])
    table.sort_values(by="processed_time_column", inplace=True)

    if table[selectedchart["x"]["name"]].duplicated().any():
        table = table.groupby(selectedchart["x"]["name"])[
            selectedchart["table"]["map_type_attr"]["numerical"]].mean().reset_index()

    return table[selectedchart["table"]["map_type_attr"]["numerical"]].to_json(orient='records')

    # if selectedchart["y"]["operation"] == "mean":
    #     table = table.groupby(selectedchart["x"]["name"])[
    #         selectedchart["table"]["map_type_attr"]["numerical"]].mean().reset_index()
    # elif selectedchart["y"]["operation"] == "sum":
    #     table = table.groupby(selectedchart["x"]["name"])[
    #         selectedchart["table"]["map_type_attr"]["numerical"]].sum().reset_index()
    # elif selectedchart["y"]["operation"] == "min":
    #     table = table.groupby(selectedchart["x"]["name"])[
    #         selectedchart["table"]["map_type_attr"]["numerical"]].min().reset_index()
    # elif selectedchart["y"]["operation"] == "max":
    #     table = table.groupby(selectedchart["x"]["name"])[
    #         selectedchart["table"]["map_type_attr"]["numerical"]].max().reset_index()

    # for attr in selectedchart["table"]["map_type_attr"]["numerical"]:
    #     if attr != selectedchart["y"]["name"]:
    #         print(table[selectedchart["y"]["name"]].corr(table[attr]))
    # print(table)
    # table[selectedchart["x"]["name"]
    #       ] = table[selectedchart["x"]["name"]].astype(str)
    # table["processed_time_column_"+selectedchart["x"]["name"]] = pd.to_datetime(
    #     table[selectedchart["x"]["name"]])
    # print(table)
    # import ast
    # d = ast.literal_eval(table.to_json(orient='records'))
    # print(d)
    # print([d[1]])
    # print(str([d[1]]))
    # print(type(d))
    # print(table.to_json(orient='records'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
