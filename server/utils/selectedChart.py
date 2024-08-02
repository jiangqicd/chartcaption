import pandas as pd
import random

# from ..annotationGenerator import annotationGenerator


class selectedChart:
    def __init__(self, table_name, tableData, map_attr_type):
        self.chart = {
            "description": "Here's a chart used to describe timing data patterns",
            "table": {"name": table_name, "x_delimited_attributes": [], "y_delimited_attributes": [], "filter_delimited_attributes": [], "map_attr_type": map_attr_type},
            "x": {"name": '', "operation": 'null'},
            "y": {"name": '', "operation": 'null'},
            "filter": {"selectedAttribute": '', "type": '', "values": []},
            "saliencyScore": [],
            "visualSaliencyFeature": [],
            "patterns": [],
            "annotations": {}
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
        self.categorical_attributes = [
            attr for attr, attr_type in self.map_attr_type.items() if attr_type == "categorical"]
        
        subset_df=self.tableData.copy()[self.categorical_attributes]
        # 计算每列的唯一值数量
        unique_counts = subset_df.nunique()

        # 对 unique_counts 进行排序，获取排序后的列名
        self.categorical_attributes = unique_counts.sort_values(ascending=True).index.tolist()

        self.map_type_attr = {"temporal": self.temporal_attributes,
                              "numerical": self.numerical_attributes, "categorical": self.categorical_attributes}
        self.chart["table"]["map_type_attr"] = self.map_type_attr

        x_delimited_attributes = []
        y_delimited_attributes = []

        for attr in self.temporal_attributes:
            x_delimited_attributes.append(
                {"name": attr, "operation": {"default": "null", "options": ["null"]}})

        for attr in self.numerical_attributes:
            y_delimited_attributes.append(
                {"name": attr, "operation": {"default": "mean", "options": ["mean", "sum", "min", "max", "null"]}})

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

        self.chart["x"]["name"] = random.choice(
            self.temporal_attributes) if self.temporal_attributes else []
        self.chart["y"]["name"] = random.choice(
            self.numerical_attributes) if self.numerical_attributes else []

        # 根据属性数据特征设置operation,目前只设置y上操作
        if self.tableData[self.chart["x"]["name"]].duplicated().any():
            # 默认为"mean"
            self.chart["y"]["operation"] = "mean"
