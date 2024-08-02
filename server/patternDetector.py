#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File:PatternDetector.py
@description:
@Time:2024/01/15 14:32:35
@Author:jiangqi
@Email:jiangqi@zjut.edu.cn
'''

from gurobipy import Model, GRB, quicksum
from scipy.stats import kendalltau
from scipy.fft import fft
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
import pandas as pd
import requests
import ast

# [('trend_down', 54, 108), ('trend_down', 139, 254)]


class patternDetector:

    def __init__(self, data):

        self.time_series = data  # data为检测时序序列
        self.subseq_scores = {}  # subseq_scores存储了所有可能子序列的评分
        self.subseq_patterns = {}  # subseq_patterns存储了所有可能子序列对应的模式

        # 目标函数权重
        self.weight_score = 10
        self.weight_width = 10
        self.weight_diff = 150
        self.weight_count = -1

        self.point_patterns = []

        # [('trend_down', 54, 108), ('trend_down', 139, 254)]
        self.line_patterns = []

    def normalized(self, arr):
        min_val = np.min(arr)
        max_val = np.max(arr)
        normalized_arr = (arr - min_val) / (max_val - min_val)

        return list(np.round(normalized_arr, 3))

    def send_post_request(self, series):
        url = "http://tablevis.zjutvis.org:45186/question"
        payload = {
            "question": series
        }

        try:
            # 发送 POST 请求，使用 form-data 形式
            response = requests.post(url, data=payload)

            # 检查响应状态码
            if response.status_code == 200:
                # 解析 JSON 响应
                data = response.json()
                return data
            else:
                print(f"请求失败，状态码：{response.status_code}")
        except requests.RequestException as e:
            print(f"请求发生异常：{e}")

    def get_line_patterns(self):
        # 从LLM获取patterns
        series = self.normalized(self.time_series)
        out = ast.literal_eval(self.send_post_request(
            str(series))['response'])
        self.line_patterns = out

        return out

    def socre_line_patterns(self):
        # to do
        print()

    def preprocessing(self, time_series):
        for i in range(len(time_series)):
            for j in range(i+1, len(time_series)):

                data = time_series[i:j+1]

                if len(set(data)) == 1:
                    trend_score = 0
                    periodicity_score = 0
                    constancy_score = 1
                else:
                    trend_score = self.get_trend_score(data)
                    periodicity_score = self.get_periodicity_score(data)
                    constancy_score = self.get_constancy_score(data)

                    score_to_pattern = {
                        trend_score: 'Trend',
                        periodicity_score: 'Periodic',
                        constancy_score: 'Stable'
                    }

                    max_score = max(score_to_pattern.keys())
                    self.subseq_scores[(i, j)] = max_score
                    self.subseq_patterns[(i, j)] = score_to_pattern[max_score]

    def get_trend_score(self, d):

        # 使用Kendall Tau测试来检验趋势显著性
        slope, _, _, _, _ = linregress(np.arange(len(d)), d)

        # 通过调整 alpha 的值，可以改变衰减的速率。
        alpha = 1

        # 计算趋势显著性分数【0，1】
        trend_score = (1-np.exp(-abs(slope*alpha))) / \
            (1 + np.exp(-abs(slope*alpha)))

        return trend_score

    def get_periodicity_score(self, d):

        # # 利用傅里叶变换
        # fft_result = fft(data)

        # # 获取幅度谱（频谱的绝对值）
        # amplitudes = np.abs(fft_result)

        # # 选择正频率部分
        # positive_amplitudes = amplitudes[:len(amplitudes)//2]

        # # 计算周期性显著性分数【0，1】
        # periodicity_score = np.max(
        #     positive_amplitudes) / np.sum(positive_amplitudes)

        # 利用自相关分析
        autocorrelation = pd.Series(d).autocorr(lag=1)
        periodicity_score = abs(autocorrelation)

        return periodicity_score

    def get_constancy_score(self, d):

        # 波动平稳性
        mean = np.mean(d)
        std_dev = np.var(d)
        cv = std_dev / mean  # Coefficient of Variation

        # Volatility significance calculation
        constancy_score = 1 - cv / (1 + cv)

        return constancy_score

    def get_point_patterns(self):

        # 最高点
        max_index = np.argmax(self.time_series)
        self.point_patterns.append(
            {"index": max_index, "pattern_type": "maximum"})
        # 最低点
        min_index = np.argmin(self.time_series)
        self.point_patterns.append(
            {"index": min_index, "pattern_type": "minimum"})
        # endpoint
        self.point_patterns.append(
            {"index": len(self.time_series)-1, "pattern_type": "endpoint"})

        # changepoint =>todo

        return self.point_patterns

    def get_line_patterns(self):

        # 创建模型
        model = Model("Time Series Optimization")

        # 决策变量
        subsequence_vars = model.addVars(len(self.time_series), len(
            self.time_series), vtype=GRB.BINARY, name="subseq")

        # 添加目标函数
        objective = quicksum(
            self.weight_score * self.subseq_scores[(i, j)] * subsequence_vars[i, j] for i, j in self.subseq_scores)
        # objective += quicksum(self.weight_width * (j - i+1) *
        #                       subsequence_vars[i, j] for i, j in self.subseq_scores)
        objective += quicksum(self.weight_count *
                              subsequence_vars[i, j] for i, j in self.subseq_scores)

        # 增加相邻子序列间得分差异性
        for i in range(len(self.time_series)):
            for j in range(i+2, len(self.time_series)):
                if (i, j-1) in self.subseq_scores and (i+1, j) in self.subseq_scores:
                    objective += self.weight_diff * \
                        abs(self.subseq_scores[(i, j-1)] - self.subseq_scores[(i+1, j)]) * \
                        subsequence_vars[i, j]

        model.setObjective(objective, GRB.MAXIMIZE)

        # #添加约束
        for k in range(len(self.time_series)):
            model.addConstr(quicksum(subsequence_vars[i, j] for i in range(k+1)
                                     for j in range(k+1, len(self.time_series)) if (i, j) in self.subseq_scores) <= 1)

        # 求解模型
        model.optimize()

        # 获取解决方案
        solution = [(i, j)
                    for i, j in self.subseq_scores if subsequence_vars[i, j].X > 0.5]

        for i, j in solution:
            self.line_patterns.append({"start_index": i, "end_index": j, "pattern_type": self.subseq_patterns[(
                i, j)], "score": self.subseq_scores[(i, j)]})

        return self.line_patterns
