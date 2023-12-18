import pandas as pd
import random


class selectedChart:
    def __init__(self, table_name, tableData, map_attr_type):
        self.chart = {
            "description": "Here's a chart used to describe timing data patterns",
            "table": {"name": table_name, "x_delimited_attributes": [], "y_delimited_attributes": [], "filter_delimited_attributes": []},
            "x": {"name": '', "operation": 'null'},
            "y": {"name": '', "operation": 'null'},
            "filter": {"selectedAttribute": '', "type": '', "values": []},
            "saliencyScore": [],
            "visualSaliencyFeature": [],
            "annotations": []
        }
        self.tableData = tableData
        self.map_attr_type = map_attr_type

        # 进行数据预处理
        self.preprocessing()

    # 用于处理表格数据，以提取其中的属性信息
    def preprocessing(self):

        self.temporal_attributes = [
            attr for attr, attr_type in self.map_attr_type.items() if attr_type == "temporal"]
        self.numerical_attributes = [
            attr for attr, attr_type in self.map_attr_type.items() if attr_type == "numerical"]

        x_delimited_attributes = []
        y_delimited_attributes = []

        for attr in self.temporal_attributes:
            x_delimited_attributes.append(
                {"name": attr, "operation": {"default": "null", "options": ["null"]}})

        for attr in self.numerical_attributes:
            if self.tableData[attr].duplicated().any():
                y_delimited_attributes.append(
                    {"name": attr, "operation": {"default": "mean", "options": ["mean", "sum", "min", "max"]}})
            else:
                y_delimited_attributes.append(
                    {"name": attr, "operation": {"default": "null", "options": ["null"]}})

        self.chart["table"]["x_delimited_attributes"] = x_delimited_attributes
        self.chart["table"]["y_delimited_attributes"] = y_delimited_attributes

        filter_delimited_attributes = []
        for attr, attr_type in self.map_attr_type.items():
            if attr_type == "categorical":
                filter_delimited_attributes.append(
                    {"name": attr, "type": "oneOf", "scope": list(self.tableData[attr].unique())})
            else:
                filter_delimited_attributes.append(
                    {"name": attr, "type": "range", "scope": [float(self.tableData[attr].min()), float(self.tableData[attr].max())]})
        self.chart["table"]["filter_delimited_attributes"] = filter_delimited_attributes


        # 用于首次呈现line chart，系统随机选取x,y属性
        self.chart["x"]["name"] = random.choice(self.temporal_attributes)
        self.chart["y"]["name"] = random.choice(self.numerical_attributes)

        # 根据属性数据特征设置operation,目前只设置y上操作
        if self.tableData[self.chart["x"]["name"]].duplicated().any():
            # 默认为"mean"
            self.chart["y"]["operation"] = "mean"