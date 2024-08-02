#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File:PatternDetector.py
@description:
@Time:2024/01/15 14:32:35
@Author:jiangqi
@Email:jiangqi@zjut.edu.cn
'''
import numpy as np
import pandas as pd
from openai import OpenAI
import requests
import ast
import pmdarima as pm
import os
from dtw import dtw
import copy
import random

os.environ["http_proxy"] = "http://127.0.0.1:10810"
os.environ["https_proxy"] = "http://127.0.0.1:10810"


class annotationGenerator:

    def __init__(self, table, chart):

        self.table = table
        self.map_attr_type = chart["table"]["map_attr_type"]
        self.line_patterns = []
        self.chart = chart
        self.x_name = chart["x"]["name"]
        self.y_name = chart["y"]["name"]
        self.x_data = []
        self.y_data = []
        self.data_details_of_presented_series = None
        self.data_aggregated_of_presented_series = None
        self.data_filter_context = {}
        self.numerical_attr_data = {}
        self.filter_obj_data = {}
        self.series_len = 0

        self.isFilter = False
        self.isAggregate = False

        # self.annotations = {
        #     "1-level": {"text_description_annotation": []},
        #     "2-level": {"detail_annotation": [], "correlation_annotation": [], "lag_annotation": [], "prediction_annotation": []}
        # }

        self.annotations = {
            "text_description_annotation": [],
            "detail_annotation": [],
            "correlation_annotation": [],
            "lag_annotation": [],
            "prediction_annotation": []
        }

        self.line_patterns_with_annotations = []
        self.get_selectedchart_information()
        self.get_chart_x_y_data(table.copy(deep=True), chart)
        self.llm_max_retries = 5

    def get_selectedchart_information(self):

        if self.chart["filter"]["selectedAttribute"] != "":
            self.isFilter = True

        if self.chart["y"]["operation"] != "null":
            self.isAggregate = True

    def get_chart_x_y_data(self, table, selectedchart):

        # 注意，table需是深拷贝进来的

        # 1. 先对表格数据按照时间顺序排序
        table[selectedchart["x"]["name"]+"_to_string"
              ] = table[selectedchart["x"]["name"]].astype(str)
        table["datetime_"+selectedchart["x"]["name"]] = pd.to_datetime(
            table[selectedchart["x"]["name"]+"_to_string"])
        table.sort_values(
            by="datetime_"+selectedchart["x"]["name"], inplace=True)

        if selectedchart["filter"]["selectedAttribute"] != "" and len(selectedchart["filter"]["values"]) != 0 and selectedchart["filter"]["type"] == "oneOf":
            filters = list(
                set(list(table[selectedchart["filter"]["selectedAttribute"]])))

            for filter in filters:
                table_copy = table.copy(deep=True)
                if filter != selectedchart["filter"]["values"][0]:
                    table_copy = table_copy[(table_copy[selectedchart["filter"]["selectedAttribute"]]
                                             == selectedchart["filter"]["values"][0])]
                    if selectedchart["y"]["operation"] == "mean":
                        table_copy = table_copy.groupby(selectedchart["x"]["name"])[
                            selectedchart["table"]["map_type_attr"]["numerical"]].mean().reset_index()
                    elif selectedchart["y"]["operation"] == "sum":
                        table_copy = table_copy.groupby(selectedchart["x"]["name"])[
                            selectedchart["table"]["map_type_attr"]["numerical"]].sum().reset_index()
                    elif selectedchart["y"]["operation"] == "min":
                        table_copy = table_copy.groupby(selectedchart["x"]["name"])[
                            selectedchart["table"]["map_type_attr"]["numerical"]].min().reset_index()
                    elif selectedchart["y"]["operation"] == "max":
                        table_copy = table_copy.groupby(selectedchart["x"]["name"])[
                            selectedchart["table"]["map_type_attr"]["numerical"]].max().reset_index()

                    self.data_filter_context[filter] = list(
                        table_copy[self.y_name])

        # 2. 获取过滤后的表格数据
        if selectedchart["filter"]["selectedAttribute"] != "":
            if selectedchart["filter"]["type"] == "oneOf":
                if len(selectedchart["filter"]["values"]) > 0:
                    table = table[(table[selectedchart["filter"]["selectedAttribute"]]
                                   == selectedchart["filter"]["values"][0])]
            else:
                if selectedchart["table"]["map_attr_type"][selectedchart["filter"]["selectedAttribute"]] == "temporal":
                    if "datetime_"+selectedchart["filter"]["selectedAttribute"] not in table.columns:
                        table[selectedchart["filter"]["selectedAttribute"]+"_to_string"
                              ] = table[selectedchart["filter"]["selectedAttribute"]].astype(str)
                        table["datetime_"+selectedchart["filter"]["selectedAttribute"]] = pd.to_datetime(
                            table[selectedchart["filter"]["selectedAttribute"]+"_to_string"])
                    selectedchart["filter"]["selectedAttribute"] = "datetime_" + \
                        selectedchart["filter"]["selectedAttribute"]
                    min_val, max_val = selectedchart["filter"]["values"]
                    min_val = pd.to_datetime(str(min_val))
                    max_val = pd.to_datetime(str(max_val))
                    table = table[(table[selectedchart["filter"]["selectedAttribute"]] >= min_val) & (
                        table[selectedchart["filter"]["selectedAttribute"]] <= max_val)]
                else:
                    min_val, max_val = selectedchart["filter"]["values"]
                    table = table[(table[selectedchart["filter"]["selectedAttribute"]] >= min_val) & (
                        table[selectedchart["filter"]["selectedAttribute"]] <= max_val)]

        self.data_details_of_presented_series = table.copy(deep=True)

        # 3. 获取聚合操作后的表格数据
        if selectedchart["y"]["operation"] == "mean":
            table = table.groupby(selectedchart["x"]["name"])[
                selectedchart["table"]["map_type_attr"]["numerical"]].mean().reset_index()
        elif selectedchart["y"]["operation"] == "sum":
            table = table.groupby(selectedchart["x"]["name"])[
                selectedchart["table"]["map_type_attr"]["numerical"]].sum().reset_index()
        elif selectedchart["y"]["operation"] == "min":
            table = table.groupby(selectedchart["x"]["name"])[
                selectedchart["table"]["map_type_attr"]["numerical"]].min().reset_index()
        elif selectedchart["y"]["operation"] == "max":
            table = table.groupby(selectedchart["x"]["name"])[
                selectedchart["table"]["map_type_attr"]["numerical"]].max().reset_index()

        self.data_aggregated_of_presented_series = table.copy(deep=True)

        if 'index' not in self.data_aggregated_of_presented_series.columns:
            self.data_aggregated_of_presented_series['index'] = self.data_aggregated_of_presented_series.index

        self.chart["table"]["data"]["form_of_records"] = self.data_aggregated_of_presented_series.to_json(
            orient='records')

        self.x_data = list(table[selectedchart["x"]["name"]])
        self.y_data = list(table[selectedchart["y"]["name"]])

        for attr in selectedchart["table"]["map_type_attr"]["numerical"]:
            self.numerical_attr_data[attr] = {"array_form": list(table[attr]), "json_form": table[[
                selectedchart["x"]["name"], attr]].to_json(orient='records')}

    def get_patterns(self):

        # 获取点型模式, ==>Todo

        # 获取线型模式
        for attr in self.numerical_attr_data.keys():
            series_data = self.numerical_attr_data[attr]["array_form"]
            series_data = self.normalized(series_data)
            self.series_len = len(series_data)
            # p = self.get_patterns_by_qwen(str(series_data))
            p = self.get_patterns_by_chatgpt(str(series_data))
            self.numerical_attr_data[attr]["pattern"] = p

        selected_keys = random.sample(list(self.data_filter_context.keys()), 7) if len(
            self.data_filter_context) > 7 else list(self.data_filter_context.keys())

        for attr in selected_keys:
            series_data = self.data_filter_context[attr]
            series_data = self.normalized(series_data)
            self.series_len = len(series_data)
            # p = self.get_patterns_by_qwen(str(series_data))
            p = self.get_patterns_by_chatgpt(str(series_data))
            self.filter_obj_data[attr] = {}
            self.filter_obj_data[attr]["data"] = self.data_filter_context[attr]
            self.filter_obj_data[attr]["pattern"] = p

        self.line_patterns = self.numerical_attr_data[self.y_name]["pattern"]

    def normalized(self, arr):
        min_val = np.min(arr)
        max_val = np.max(arr)
        normalized_arr = (arr - min_val) / (max_val - min_val)

        return list(np.round(normalized_arr, 3))

    def get_patterns_by_chatgpt(self, series):
        prompt = f'''You are an expert in temporal data analysis. The user will provide a temporal sequence in the form of an array. Your task is to recognize and extract the temporal patterns in the data by following the steps outlined below. Respond with an array of tuples (pattern_type, start_index, end_index) representing the identified patterns, which should be directly parsable by ast.literal_eval() in Python without any additional processing.
                    ===
                    #Patterns:

                    'trend_up': Gradual increase over time, can be linear or curved.
                    'trend_down': Gradual decrease over time, can be linear or curved.
                    'cyclic': Repetitive fluctuations at roughly fixed intervals.
                    'spike-top': Ascent to a peak followed by a descent, mountain-like shape.
                    'spike-bottom': Descent to a trough followed by an ascent, valley-like shape.
                    'double_peak_top': Two adjacent peaks with a slight dip between them.
                    'double_peak_bottom': Two adjacent troughs with a slight rise between them.
                    ===
                    #Steps:

                    Analyze the global and local contextual features of the given temporal sequence.
                    #Patterns. In this process, you need to consider the trends of the data points checking their shapes and characteristics.
                    Recognize patterns present in given temporal sequence based on the descriptions in
                    Generate the output array of tuples following the required format, covering all detected patterns.
                    Let's think step by step.
                    User will parse the content of your response with ast.literal_eval() directly without further process. Response one array object without any additional words. Your array object must contain all the patterns you recognize and their start and end indexes in the input timing sequence.
                    ===
                    #Examples:
                    -----
                    User input:
                    [0.403,0.416,0.396,0.399,0.399,0.391,0.378,0.39,0.381,0.379,0.362,0.345,0.339,0.328,0.317,0.31,0.3,0.288,0.265,0.26,0.281,0.271,0.261,0.26,0.266,0.264,0.264,0.275,0.26,0.264,0.267,0.265,0.262,0.264,0.263,0.273,0.29,0.299,0.315,0.346,0.377,0.425,0.471,0.473,0.468,0.469,0.474,0.469,0.469,0.47,0.478,0.492,0.523,0.559,0.625,0.696,0.783,0.776,0.785,0.778,0.775,0.794,0.794,0.812,0.785,0.731,0.676,0.581,0.359,0.0,0.932,0.971,0.967,0.97,0.932,0.976,0.974,0.959,0.975,0.983,0.978,0.982,0.966,0.959,1.0,0.98,0.966,0.986,0.954,0.959,0.974,0.967,0.941,0.971,0.957,0.95,0.939,0.968]

                    Response:
                    [('trend_down', 1, 18), ('trend_up', 34, 42),
                      ('trend_up', 47, 56), ('spike-bottom', 63, 72)]
                    -----
                    User input:
                    [0.745,0.749,0.746,0.748,0.742,0.91,1.0,0.945,0.785,0.608,0.496,0.51,0.648,0.84,0.976,0.994,0.877,0.693,0.538,0.489,0.574,0.742,0.732,0.742,0.746,0.757,0.74,0.739,0.743,0.742,0.687,0.626,0.503,0.339,0.088,0.207,0.292,0.351,0.353,0.309,0.259,0.17,0.095,0.0,0.163,0.301,0.41,0.508,0.568,0.576,0.587,0.582,0.546,0.563,0.581,0.518,0.527,0.558,0.588,0.568,0.552,0.562,0.563]

                    Response:
                    [('cyclic', 4, 21), ('double_peak_bottom', 29, 48)]
                    -----
                    User input:
                    [0.584,0.591,0.587,0.584,0.568,0.544,0.474,0.358,0.363,0.369,0.359,0.532,0.69,0.466,0.465,0.463,0.388,0.254,0.0,0.008,0.006,0.0,0.001,0.458,0.908,0.559,0.691,0.857,1.0,0.334,0.35,0.335,0.324,0.345,0.341,0.34,0.346,0.326]

                    Response:
                    [('trend_down', 3, 7), ('spike-top', 10, 13),
                      ('trend_down', 15, 18), ('double_peak_top', 22, 29)]
                    ===
                    #Constraints: You only need to describe the patterns contained in #Patterns. You need to make sure that the start and end indexes identified are correct and not outside the time series range. You also need to ensure that there is no overlap in the scope of each pattern. Response the array object directly without any other contents. Make sure it can be directly parsed by ast.literal_eval() in JavaScript. Write your description in one line without any \n.
                    ===
                    #Input series:
                    {series}

                    ===
                    Some examples provided in #Examples are just for you to study and have nothing to do with input sequence. Now, you should follow the #Steps, analyze the #Input series, and return the array of identified patterns. Focus on precision and conciseness in your output.'''
        out = []
        retries = 0

        while len(out) == 0 and retries < self.llm_max_retries:
            print("*********************************")
            try:
                res = self.send_request_to_llm(prompt)
                res = ast.literal_eval(res)
                out = res
            except Exception as e:
                print("解析失败，错误:", e)
                retries += 1

        return out

    def get_patterns_by_qwen(self, series):
        url = "http://demo2.zjutvis.org:45186/upload"
        payload = {
            "question": series
        }
        try:
            # 发送 POST 请求，使用 form-data 形式
            response = requests.post(url, data=payload)

            # 检查响应状态码
            if response.status_code == 200:
                # 解析 JSON 响应
                data = response.json()['response']
                out = ast.literal_eval(data)
                final_out = []
                for i in out:
                    final_out.append([i[0], i[1][0], i[1][-1]])
                # 遍历二维列表的每一行
                for i in range(len(final_out)):
                    # 检查第2个和第3个元素是否都大于25
                    if final_out[i][1] > self.series_len-1:
                        # 将第2个和第3个元素的值设置为25
                        final_out[i][1] = self.series_len-1
                    if final_out[i][2] > self.series_len-1:
                        # 将第2个和第3个元素的值设置为25
                        final_out[i][2] = self.series_len-1
                out = final_out
                return out
            else:
                print(f"请求失败，状态码：{response.status_code}")
        except requests.RequestException as e:
            print(f"请求发生异常：{e}")

    def generate(self):
        print("**************************正在提取模式***************************")
        self.get_patterns()
        for p in self.line_patterns:
            self.line_patterns_with_annotations.append(
                {"pattern": p[0], "start": p[1], "end": p[2], "annotations": copy.deepcopy(self.annotations)})
        # 执行注释
        print("**************************正在生成文本注释***************************")
        self.text_description_annotation()
        print("**************************正在生成详情注释***************************")
        self.detail_annotation()
        print("**************************正在生成相关性注释***************************")
        self.correlation_annotation()
        print("**************************正在生成lag注释***************************")
        self.lag_annotation()
        print("**************************正在生成预测注释***************************")
        self.prediction_annotation()

        self.chart["table"]["data"]["data_filter_context"] = self.data_filter_context
        self.chart["annotations"] = self.annotations
        self.chart["line_patterns_with_annotations"] = self.line_patterns_with_annotations

    def send_request_to_llm(self, text):

        # openai.api_base = "https://api5.ai-gaochao.net/v1"
        # openai.api_key = "sk-W4WEvF69mduCwbuHE2D0Bc27616d4085Ba249235DbBa8a36"

        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "user", "content": text}
        #     ]
        # )

        client = OpenAI(
            # api_key="sk-hIz6RjXZeE8UwpQnLwapbfkOZ1MwO164YmT5dkrwsghTfk0p",
            # base_url="https://api.moonshot.cn/v1",
            # base_url="https://api5.ai-gaochao.net/v1",
            # api_key="sk-W4WEvF69mduCwbuHE2D0Bc27616d4085Ba249235DbBa8a36",
            base_url="https://api.gpts.vin/v1",
            api_key="sk-D7bON6bZXvkHiRsd3d6448BeA9B24c9eAd3a5eD447Ec76D2"
        )

        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            # model="moonshot-v1-8k",
            model="gpt-4",
            messages=[
                {"role": "user", "content": text}
            ]
        )

        description = response.choices[0].message.content

        return description

    def text_description_annotation_prompt_generation(self, x_name, x_data, y_name, y_data, pattern_type):
        text = (
            "现在需要你帮我描述时序序列中的模式,我会告诉你时序序列的数据以及它的模式类型,然后需要你输出详尽的描述文字,你需要输出英文。 "
            "***时序序列信息*** "
            f"#x轴上的属性是{x_name}# "
            f"#x轴上的数据是{', '.join(map(str, x_data))}# "
            f"#y轴上的属性是{y_name}# "
            f"#y轴上的数据是{', '.join(map(str, y_data))}# "
            f"***模式类型*** #该序列呈现的模式类型为：{pattern_type}#"
            "注意: 你输出的文本描述需要精炼一些突出重要信息,输出两句话,输出英文"
        )
        return text

    def text_description_annotation(self):
        for index, p in enumerate(self.line_patterns):
            # 利用大模型生成时间序列模式文本描述
            p_x_data = list(self.x_data[int(p[1]):int(p[2])+1])
            p_y_data = list(self.y_data[int(p[1]):int(p[2])+1])
            prompt = self.text_description_annotation_prompt_generation(
                self.x_name, p_x_data, self.y_name, p_y_data, p[0])
            text_description = self.send_request_to_llm(prompt)
            annotation = {"start": str(p[1]), "end": str(
                p[2]), "description": text_description}
            self.line_patterns_with_annotations[index]["annotations"]["text_description_annotation"] = annotation
            self.annotations["text_description_annotation"].append(
                {"type": str(p[0]), "start": str(p[1]), "end": str(p[2]), "annotation": annotation})

            # 利用规则生成时间序列模式文本描述,结果更可控
            # if p[0] == "trend_up":
            #     text_description = ""
            # elif [0] == "trend_down":
            #     text_description = ""
            # elif [0] == "cyclic":
            #     text_description = ""
            # elif [0] == "spike-top":
            #     text_description = ""
            # elif [0] == "spike-bottom":
            #     text_description = ""
            # elif [0] == "double_peak_top":
            #     text_description = ""
            # elif [0] == "double_peak_bottom":
            #     text_description = ""
            # else:
            #     text_description = ""

    def detail_annotation(self):

        # 首先判断是否有重复的时序标签，详情注释只发生在有重复时序标签
        if len(list(set(self.data_details_of_presented_series[self.x_name]))) != len(list(self.data_details_of_presented_series[self.x_name])) and self.chart["y"]["operation"] != "null":
            for index, p in enumerate(self.line_patterns):
                start = self.x_data[int(p[1])]
                end = self.x_data[int(p[2])]
                data_details = self.get_pattern_detail_data(
                    self.data_details_of_presented_series.copy(deep=True), start, end)
                annotation = {"start": str(p[1]), "end": str(
                    p[2]), "data_details": data_details}
                self.line_patterns_with_annotations[index]["annotations"]["detail_annotation"] = annotation
                self.annotations["detail_annotation"].append(
                    {"type": str(p[0]), "start": str(p[1]), "end": str(p[2]), "annotation": annotation})

    def get_pattern_detail_data(self, table, min_val, max_val):
        min_val = pd.to_datetime(str(min_val))
        max_val = pd.to_datetime(str(max_val))
        table = table[(table["datetime_"+self.chart["x"]["name"]] >= min_val) & (
            table["datetime_"+self.chart["x"]["name"]] <= max_val)]

        table = table[self.chart["table"]["map_type_attr"]
                      ["categorical"] + [self.x_name, self.y_name]]
        return table.to_json(orient='records')

    def correlation_annotation(self):

        for index, p in enumerate(self.line_patterns):
            annotations = {"attr_attr": [], "obj_obj": []}

            table = self.data_aggregated_of_presented_series.copy(
                deep=True)
            # start = self.x_data[int(p[1])]
            # end = self.x_data[int(p[2])+1]
            # min_val = pd.to_datetime(str(start))
            # max_val = pd.to_datetime(str(end))
            # table[self.chart["x"]["name"]+"_to_string"
            #       ] = table[self.chart["x"]["name"]].astype(str)
            # table["datetime_"+self.chart["x"]["name"]] = pd.to_datetime(
            #     table[self.chart["x"]["name"]+"_to_string"])
            # table = table[(table["datetime_"+self.chart["x"]["name"]] >= min_val) & (
            #     table["datetime_"+self.chart["x"]["name"]] <= max_val)]

            for attr in self.chart["table"]["map_type_attr"]["numerical"]:
                if attr != self.chart["y"]["name"]:
                    # correlation = self.table[self.chart["y"]
                    #                          ["name"]].corr(self.table[attr])
                    # correlations.append(
                    #     {"attr": attr, "corr": correlation, "data": {"array_form": list(table[attr]), "json_form": table[[
                    #         self.chart["x"]["name"], attr]].to_json(orient='records')}})

                    array1 = list(table[attr])[int(p[1]):int(p[2]+1)]
                    array2 = list(table[self.y_name])[
                        int(p[1]):int(p[2]+1)]

                    correlation = round(
                        np.corrcoef(array1, array2)[0, 1], 2)

                    # correlations.append(
                    #     {"attr": attr, "corr": correlation, "data": {"array_form": array1, "json_form": table[[
                    #         self.chart["x"]["name"], attr]].to_json(orient='records')}})
                    annotations["attr_attr"].append(
                        {"attr": attr, "corr": correlation, "start": str(p[1]), "end": str(
                            p[2])})
            if self.chart["filter"]["type"] == "oneOf" and self.isFilter:
                for attr, value in self.data_filter_context.items():
                    array1 = value[int(p[1]):int(p[2]+1)]
                    array2 = list(table[self.y_name])[
                        int(p[1]):int(p[2]+1)]

                    correlation = round(
                        np.corrcoef(array1, array2)[0, 1], 2)
                    annotations["obj_obj"].append(
                        {"attr": attr, "corr": correlation, "start": str(p[1]), "end": str(
                            p[2])})

            self.line_patterns_with_annotations[index]["annotations"]["correlation_annotation"] = annotations
            self.annotations["correlation_annotation"].append(
                {"type": str(p[0]), "start": str(p[1]), "end": str(p[2]), "annotation": annotations})

    def lag_annotation(self):

        # 获取上下文模式集合
        attr_pattern_context_set = {"trend_up": [], "trend_down": [], "cyclic": [], "spike-top": [],
                                    "spike-bottom": [], "double_peak_top": [], "double_peak_bottom": []}
        for attr in self.numerical_attr_data.keys():
            if attr != self.y_name:
                for p in self.numerical_attr_data[attr]["pattern"]:
                    attr_pattern_context_set[p[0]].append(
                        {"attr": attr, "start": p[1], "end": p[2]})

        obj_pattern_context_set = {"trend_up": [], "trend_down": [], "cyclic": [], "spike-top": [],
                                   "spike-bottom": [], "double_peak_top": [], "double_peak_bottom": []}
        for attr in self.filter_obj_data.keys():
            if attr != self.chart["filter"]["values"][0]:
                for p in self.filter_obj_data[attr]["pattern"]:
                    obj_pattern_context_set[p[0]].append(
                        {"attr": attr, "start": p[1], "end": p[2]})

        for index, m_p in enumerate(self.line_patterns):

            annotations = {"attr_attr": [], "obj_obj": []}

            m = self.y_data[int(m_p[1]):int(m_p[2])+1]

            attr_lags = []

            for n_p in attr_pattern_context_set[m_p[0]]:
                n = self.numerical_attr_data[n_p["attr"]]["array_form"][int(
                    n_p["start"]):int(n_p["end"])+1]
                d = self.get_similarity_between_sequences(m, n)
                if d < 1:
                    # data_json_form = ast.literal_eval(
                    #     self.numerical_attr_data[n_p["attr"]]["array_form"])
                    # data_json_form = data_json_form[int(
                    #     n_p["start"]):int(n_p["end"])+1]
                    # lags.append({"attr": n_p["attr"], "start": n_p["start"], "end": n_p["end"], "dist": d, "data": {
                    #             "array_form": n, "json_form": data_json_form}})
                    attr_lags.append(
                        {"attr": n_p["attr"], "start": n_p["start"], "end": n_p["end"], "dist": d})

            attr_lags = sorted(attr_lags, key=lambda x: x["dist"])
            annotations["attr_attr"] = attr_lags

            obj_lags = []
            for n_p in obj_pattern_context_set[m_p[0]]:
                n = self.filter_obj_data[n_p["attr"]]["data"][int(
                    n_p["start"]):int(n_p["end"])+1]
                d = self.get_similarity_between_sequences(m, n)
                if d < 1:
                    # data_json_form = ast.literal_eval(
                    #     self.numerical_attr_data[n_p["attr"]]["array_form"])
                    # data_json_form = data_json_form[int(
                    #     n_p["start"]):int(n_p["end"])+1]
                    # lags.append({"attr": n_p["attr"], "start": n_p["start"], "end": n_p["end"], "dist": d, "data": {
                    #             "array_form": n, "json_form": data_json_form}})
                    obj_lags.append(
                        {"attr": n_p["attr"], "start": n_p["start"], "end": n_p["end"], "dist": d})

            obj_lags = sorted(obj_lags, key=lambda x: x["dist"])
            annotations["obj_obj"] = obj_lags

            self.line_patterns_with_annotations[index]["annotations"]["lag_annotation"] = annotations
            self.annotations["lag_annotation"].append(
                {"type": str(m_p[0]), "start": str(m_p[1]), "end": str(m_p[2]), "annotation": annotations})

    def manhattan_distance(self, x, y):
        return np.abs(x - y).sum()

    def get_similarity_between_sequences(self, m, n):

        m = self.normalized(m)
        n = self.normalized(n)

        # 使用曼哈顿距离作为距离度量
        # 计算DTW距离
        d = dtw(m, n, dist=self.manhattan_distance)[0]

        return d

    def prediction_annotation(self):

        data_series = np.array(self.y_data)

        # 使用auto_arima自动选择模型参数并拟合模型
        model = pm.auto_arima(
            data_series,
            test='adf',       # 使用ADF检验确定差分阶数
            max_p=5, max_q=5,  # 设置p和q的最大搜索值
            stepwise=True,   # 使用步进式搜索策略
            suppress_warnings=True,
            error_action='ignore'
        )

        # 模型训练
        model.fit(data_series)

        # 计算预测的期数，即原序列长度的1/5
        forecast_horizon = int(len(data_series) / 5)

        # 预测未来的数据
        forecast, conf_int = model.predict(
            n_periods=forecast_horizon, return_conf_int=True)

        forecast = list(
            np.insert(forecast, 0, data_series[len(data_series)-1]))

        conf_int = list(conf_int)

        new_array = np.array([data_series[len(data_series)-1],
                              data_series[len(data_series)-1]])
        conf_int.insert(0, new_array)

        # 将conf_int分解为上界和下界
        lower_bounds = [ci[0] for ci in conf_int]
        upper_bounds = [ci[1] for ci in conf_int]

        text = "给定一个时间序列数组:"
        text += str(self.x_data)
        text += "你需要参考数组中序列顺序,在这个序列基础上再生成"+str(forecast_horizon)+"个序列数据."
        text += "你只需要需要返回给我你生成的序列给我,按照数组形式,你只需要给我生成的序列数组."
        text += "#接下来,我会告诉告诉你一些例子。序列数据:[2012-10,2012-11,2012-12,2013-01],生成序列长度:2,你输出的结果:[2013-02,2013-03]"
        text += "序列数据:[2012-10-29,2012-10-30,2012-10-31,2012-11-01],生成序列长度:2,你输出的结果:[2012-11-02,2012-11-03]"
        text += "序列数据:[星期四,星期五,星期六,星期日],生成序列长度:2,你输出的结果:[星期一,星期二]"
        text += "序列数据:[1972,1973,1974,1975],生成序列长度:2,你输出的结果:[1976,1977]"
        text += "==注意：你只需要需要返回给我你生成的序列给我,它是数组形式.你只需要返回生成的序列数组,除此之外,你不要回复任何其它文字."

        retries = 0

        x_forecast = []

        while len(x_forecast) != forecast_horizon and retries < self.llm_max_retries:

            try:
                res = self.send_request_to_llm(text)
                print(res)
                res = ast.literal_eval(res)
                x_forecast = res
            except Exception as e:
                print("解析失败，错误:", e)
                retries += 1
                if retries == self.llm_max_retries:
                    for i in range(forecast_horizon):
                        x_forecast.append("FS-"+str(i+1))

        x_forecast.insert(0, self.x_data[-1])

        text = "给定一个原始序列数据:"
        text += str(data_series)
        text += "以及预测得到的结果序列数据:"
        text += str(forecast)
        text += "现在,你需要描述预测得到的结果序列数据的变化趋势."
        text += "#你需要输出英文#"

        prediction_description = self.send_request_to_llm(text)

        self.line_patterns_with_annotations.append(
            {"pattern": "prediction", "start":len(self.x_data)-1,"end":len(self.x_data)-1+forecast_horizon,"index": len(self.x_data)-1, "annotations": {"prediction_annotation": {"prediction_data": str(forecast), "x_data": x_forecast, "prediction_upper": str(upper_bounds), "prediction_lower": str(lower_bounds), "description": prediction_description}}})
        self.annotations["prediction_annotation"].append({"type": "prediction", "index": str(
            len(self.x_data)-1), "prediction_data": str(forecast), "x_data": x_forecast, "prediction_upper": str(upper_bounds), "prediction_lower": str(lower_bounds), "description": prediction_description})
