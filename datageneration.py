import numpy as np
import matplotlib.pyplot as plt
import random
import json


def linear_interpolation(x_start, x_end, y_start, y_end):

    interpolation = np.linspace(y_start, y_end, x_end - x_start)

    return interpolation


def exp_interpolation(x_start, x_end, y_start, y_end):

    y_min = np.min([y_start, y_end])
    y_max = np.max([y_start, y_end])
    linear_space = np.linspace(y_start, y_end, x_end - x_start)
    nonlinear_space = np.exp(np.array(linear_space)*random.randint(2, 5))

    if len(nonlinear_space) < 2:
        nonlinear_space[:] = y_max
        interpolation = nonlinear_space
    else:
        min_val = np.min(nonlinear_space)
        max_val = np.max(nonlinear_space)

        # 将序列标准化到新的区间
        interpolation = ((nonlinear_space - min_val) /
                         (max_val - min_val)) * (y_max - y_min) + y_min

    return interpolation


def power_interpolation(x_start, x_end, y_start, y_end):

    y_min = np.min([y_start, y_end])
    y_max = np.max([y_start, y_end])

    linear_space = np.linspace(y_start, y_end, x_end - x_start)
    nonlinear_space = np.power(linear_space, random.randint(2, 5))

    if len(nonlinear_space) < 2:
        nonlinear_space[:] = y_max
        interpolation = nonlinear_space
    else:
        min_val = np.min(nonlinear_space)
        max_val = np.max(nonlinear_space)

        # 将序列标准化到新的区间
        interpolation = ((nonlinear_space - min_val) /
                         (max_val - min_val)) * (y_max - y_min) + y_min

    return interpolation


def cubic_spline_interpolation(x_start, x_end, y_start, y_end):

    y_min = np.min([y_start, y_end])
    y_max = np.max([y_start, y_end])

    linear_space = np.linspace(y_start, y_end, x_end - x_start)
    nonlinear_space = random.randint(2, 10)*np.power(linear_space, 3) + random.randint(
        2, 10) * np.power(linear_space, 2) + random.randint(2, 10) * np.array(linear_space)

    if len(nonlinear_space) < 2:
        nonlinear_space[:] = y_max
        interpolation = nonlinear_space
    else:
        min_val = np.min(nonlinear_space)
        max_val = np.max(nonlinear_space)

        # 将序列标准化到新的区间
        interpolation = ((nonlinear_space - min_val) /
                         (max_val - min_val)) * (y_max - y_min) + y_min

    return interpolation


def add_trend_up(x_start, x_end, y_start, y_end):

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }
    chosen_method = random.choice(list(methods.keys()))

    result = methods[chosen_method](x_start, x_end, y_start, y_end)

    return result


def add_trend_down(x_start, x_end, y_start, y_end):

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }
    chosen_method = random.choice(list(methods.keys()))

    result = methods[chosen_method](x_start, x_end, y_start, y_end)

    return result


def add_cyclic(x_start, x_end, amplitude):

    l = x_end-x_start

    if random.choice(["sin", "cos"]) == "sin":
        result = amplitude * \
            np.sin(np.linspace(0, min(random.randint(2, 10), l-1) * np.pi, l))
    else:
        result = amplitude * \
            np.cos(np.linspace(0, min(random.randint(2, 10), l-1) * np.pi, l))

    return result


def add_spike_top(x_start, x_end, y_start, y_end):

    x_mid = (x_start + x_end) // 2

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }
    chosen_method = random.choice(list(methods.keys()))

    if (x_start + x_end) % 2 == 0:
        result_left = methods[chosen_method](x_start, x_mid+1, 0, y_end)
        result_right = methods[chosen_method](
            x_mid, x_end, y_end, random.uniform(-y_start, y_start))[1:]
    else:
        if random.choice([0, 1]) == 1:
            result_left = methods[chosen_method](
                x_start, x_mid+1, 0, y_end)
            result_right = methods[chosen_method](
                x_mid, x_end, y_end, random.uniform(-y_start, y_start))[1:]
        else:
            result_left = methods[chosen_method](
                x_start, x_mid+2, 0, y_end)
            result_right = methods[chosen_method](
                x_mid, x_end, y_end, random.uniform(-y_start, y_start))[2:]

    result = np.concatenate((result_left, result_right))

    return result


def add_spike_bottom(x_start, x_end, y_start, y_end):

    x_mid = (x_start + x_end) // 2

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }
    chosen_method = random.choice(list(methods.keys()))

    if (x_start + x_end) % 2 == 0:
        result_left = methods[chosen_method](x_start, x_mid+1, 0, y_end)
        result_right = methods[chosen_method](
            x_mid, x_end, y_end, random.uniform(-y_start, y_start))[1:]
    else:
        if random.choice([0, 1]) == 1:
            result_left = methods[chosen_method](
                x_start, x_mid+1, 0, y_end)
            result_right = methods[chosen_method](
                x_mid, x_end, y_end, random.uniform(-y_start, y_start))[1:]
        else:
            result_left = methods[chosen_method](
                x_start, x_mid+2, 0, y_end)
            result_right = methods[chosen_method](
                x_mid, x_end, y_end, random.uniform(-y_start, y_start))[2:]

    result = np.concatenate((result_left, result_right))

    return result


def add_double_peak_top(x_start, x_end, y_start, y_end):

    # y_min = np.min([y_start, y_end])
    # y_max = np.max([y_start, y_end])

    # y_mid = random.uniform(0.4, 0.7)*(y_max-y_min)+y_min

    y_mid = random.uniform(0.4, 0.7)*y_end

    x_mid1 = int(x_start + random.uniform(0.8, 1.2) * (x_end - x_start) // 4)
    x_mid2 = int(x_start + random.uniform(1.8, 2.2) * (x_end - x_start) // 4)
    x_mid3 = int(x_start + random.uniform(2.8, 3.2) * (x_end - x_start) // 4)

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }

    y_top_1 = random.uniform(1.2, 1.5)
    y_top_2 = random.uniform(1.2, 1.5)

    chosen_method = random.choice(list(methods.keys()))
    result_1 = methods[chosen_method](x_start, x_mid1+1, 0, y_top_1)
    result_2 = methods[chosen_method](x_mid1, x_mid2, y_top_1, y_mid)[1:]
    result_3 = methods[chosen_method](x_mid2, x_mid3+1, y_mid, y_top_2)
    result_4 = methods[chosen_method](
        x_mid3, x_end, y_top_2, random.uniform(-y_start, y_start))[1:]

    result = np.concatenate((result_1, result_2, result_3, result_4))
    return result


def add_double_peak_bottom(x_start, x_end, y_start, y_end):

    # y_min = np.min([y_start, y_end])
    # y_max = np.max([y_start, y_end])

    # y_mid = random.uniform(0.4, 0.7)*(y_max-y_min)+y_min
    y_mid = random.uniform(0.4, 0.7)*y_end

    x_mid1 = int(x_start + random.uniform(0.8, 1.2) * (x_end - x_start) // 4)
    x_mid2 = int(x_start + random.uniform(1.8, 2.2) * (x_end - x_start) // 4)
    x_mid3 = int(x_start + random.uniform(2.8, 3.2) * (x_end - x_start) // 4)

    methods = {
        'linear': linear_interpolation,
        'exp': exp_interpolation,
        'power': power_interpolation,
        'cubic': cubic_spline_interpolation
    }
    y_top_1 = random.uniform(1.2, 1.5)
    y_top_2 = random.uniform(1.2, 1.5)

    chosen_method = random.choice(list(methods.keys()))
    result_1 = methods[chosen_method](x_start, x_mid1+1, 0, y_top_1)
    result_2 = methods[chosen_method](x_mid1, x_mid2, y_top_1, y_mid)[1:]
    result_3 = methods[chosen_method](x_mid2, x_mid3+1, y_mid, y_top_2)
    result_4 = methods[chosen_method](
        x_mid3, x_end, y_top_2, random.uniform(-y_start, y_start))[1:]

    result = np.concatenate((result_1, result_2, result_3, result_4))
    return result


def generate_series(length, patterns, l, s):
    # series = np.random.normal(loc=0.5, scale=0.1, size=length)
    series = np.random.normal(loc=l, scale=s, size=length)
    annotations = []

    for pattern_name, start, end in patterns:
        if pattern_name == "trend_up":
            series[start:end+1] += add_trend_up(start,
                                                end+1, 0, random.uniform(1, 1.5))

            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])
        elif pattern_name == "trend_down":
            series[start:end+1] -= add_trend_down(start,
                                                  end+1, 0, random.uniform(1, 1.5))
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])
        elif pattern_name == "cyclic":

            res = add_cyclic(start, end+1, random.uniform(1.2, 1.5))

            series[start:end+1] += res
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            if abs(res[0]) < 0.00001:
                annotations.append([pattern_name, start, end])
            else:
                if start != 0:
                    start = start-1
                annotations.append([pattern_name, start, end])
        elif pattern_name == "spike-top":
            series[start:end+1] += add_spike_top(
                start, end+1, 0.5, random.uniform(1.2, 1.5))
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])
        elif pattern_name == "spike-bottom":
            series[start:end+1] -= add_spike_bottom(
                start, end+1, 0.5, random.uniform(1.2, 1.5))
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])
        elif pattern_name == "double_peak_top":
            series[start:end+1] += add_double_peak_top(
                start, end+1, 0.5, random.uniform(1.2, 1.5))
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])
        elif pattern_name == "double_peak_bottom":
            series[start:end+1] -= add_double_peak_bottom(
                start, end+1, 0.5, random.uniform(1.2, 1.5))
            # if start != 0:
            #     start = start-1
            series[end+1:] = np.random.normal(loc=series[end],
                                              scale=random.uniform(0.01, 0.05), size=(length-end-1))
            annotations.append([pattern_name, start, end])

        series = normalize_array(series)
    print(length, annotations)
    return series, annotations


def normalize_array(arr):
    # 转换为numpy数组
    arr = np.array(arr)
    # 计算最小值和最大值
    min_val = np.min(arr)
    max_val = np.max(arr)
    # 进行归一化
    normalized_arr = (arr - min_val) / (max_val - min_val)
    return normalized_arr


def generate_random_intervals(sequence_length):

    n = random.randint(1, 5)  # 随机选择区间数量
    intervals = []
    current_start = random.randint(0, sequence_length // 4)

    while len(intervals) < n:

        # 计算宽度范围
        min_width = sequence_length // (n * 3)
        max_width = sequence_length // n

        if max_width < min_width:
            break

        current_width = random.randint(max(1, min_width), max(1, max_width))

        current_end = current_start + current_width

        # 检查区间是否超出序列长度
        if current_end > sequence_length-1:
            break

        intervals.append((current_start, current_end))

        # 更新下一个区间的起始位置
        current_start = random.randint(
            current_end+1, max((sequence_length-current_end) // 4, 1)+current_end)

    return intervals


def main():

    dataset_1 = []
    dataset_2 = []
    dataset_V2 = []
    dataset_V3 = []
    dataset_V4 = []
    dataset_V5 = []
    dataset_categorization = []
    dataset_segmentation = []

    # m_values = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]
    # n_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]

    # m_values = [10, 100, 200, 300]
    # n_values = [100, 200, 300, 340]

    m_values = [10]
    n_values = [100]

    id = 0
    for j in range(len(m_values)):
        while (len(dataset_2) < 50*(j+1)):
            id += 1
            # 序列
            sequence_length = random.randint(m_values[j], n_values[j])

            if sequence_length < 200:
                # l = random.uniform(0.1, 0.5)
                # s = random.uniform(0.005, 0.01)
                l = random.uniform(0.1, 0.5)
                s = random.uniform(0.01, 0.05)
            else:
                l = random.uniform(0.1, 0.5)
                s = random.uniform(0.05, 0.1)

            intervals = generate_random_intervals(sequence_length)

            patterns = ["trend_up", "trend_down", "cyclic", "spike-top",
                        "spike-bottom", "double_peak_top", "double_peak_bottom"]

            # updated_intervals = [(random.choice(patterns),) +
            #                      interval for interval in intervals]

            updated_intervals = [
                (random.choice(
                    ["trend_up", "trend_down", "cyclic", "spike-top",
                     "spike-bottom", "double_peak_top", "double_peak_bottom"]
                    if interval[1] - interval[0] >= 5 else
                    ["trend_up", "trend_down",
                        "spike-top", "spike-bottom"]
                    if 5 > interval[1] - interval[0] >= 3 else
                    ["trend_up", "trend_down"]
                ),) + interval
                for interval in intervals
            ]

            # Generate series

            if len(updated_intervals) > 0:
                print("++++++++++++++++++++++++++++++++++++++++++")
                print(id)
                series, annotations = generate_series(
                    sequence_length, updated_intervals, l, s)

                series = np.round(series, 3)
                series = list(series)

                annotations = [
                    elem for idx, elem in enumerate(annotations)
                    if not (elem[0] == "cyclic" and
                            np.max(series[elem[1]:elem[2]+1]) - np.min(series[elem[1]:elem[2]+1]) < 0.04)
                ]

                # selected_index = []

                # for i in range(len(annotations)):
                #     selected_index.append(annotations[i][1])
                #     selected_index.append(annotations[i][2])

                for i in range(len(annotations)):
                    start = annotations[i][1]
                    end = annotations[i][2]
                    s = 0.02
                    if annotations[i][0] == "trend_up":
                        # if start != 0 and series[start-1]+s < series[start]:
                        #     start -= 1

                        # start
                        if i != 0:
                            if annotations[i-1][0] == "trend_down" and annotations[i][1]-annotations[i-1][2] == 1 and series[annotations[i][1]] > series[annotations[i-1][2]]:
                                start -= 1
                            else:
                                for k in range(annotations[i][1], annotations[i-1][2], -1):
                                    if series[k] > series[k-1]+s:
                                        start -= 1
                                    else:
                                        break
                        else:
                            for k in range(annotations[i][1], 0, -1):
                                if series[k] > series[k-1]+s/2:
                                    start -= 1
                                else:
                                    break
                        # end
                        if i != len(annotations)-1:
                            if annotations[i+1][0] == "trend_down" and annotations[i+1][1]-annotations[i][2] == 1 and series[annotations[i+1][1]] > series[annotations[i][2]]:
                                end += 1
                            else:
                                for k in range(annotations[i][2]+1, annotations[i+1][1]):
                                    if series[k] > series[k-1]+s:
                                        end += 1
                                    else:
                                        break

                        else:
                            for k in range(annotations[i][2]+1, len(series)):
                                if series[k] > series[k-1]+s/2:
                                    end += 1
                                else:
                                    break
                    elif annotations[i][0] == "trend_down":
                        # if start != 0 and series[start-1] > series[start]+s:
                        #     start -= 1

                        # start
                        if i != 0:
                            if annotations[i-1][0] == "trend_up" and annotations[i][1]-annotations[i-1][2] == 1 and series[annotations[i][1]] < series[annotations[i-1][2]]:
                                start -= 1
                            else:
                                for k in range(annotations[i][1], annotations[i-1][2], -1):
                                    if series[k]+s < series[k-1]:
                                        start -= 1
                                    else:
                                        break
                        else:
                            for k in range(annotations[i][1], 0, -1):
                                if series[k]+s/2 < series[k-1]:
                                    start -= 1
                                else:
                                    break
                        if i != len(annotations)-1:
                            if annotations[i+1][0] == "trend_up" and annotations[i+1][1]-annotations[i][2] == 1 and series[annotations[i+1][1]] < series[annotations[i][2]]:
                                end += 1
                            else:
                                for k in range(annotations[i][2]+1, annotations[i+1][1]):
                                    if series[k]+s < series[k-1]:
                                        end += 1
                                    else:
                                        break
                        else:
                            for k in range(annotations[i][2]+1, len(series)):
                                if series[k]+s/2 < series[k-1]:
                                    end += 1
                                else:
                                    break
                        # if end+1 < len(series):
                        #     if series[end+1]+s < series[end]:
                        #         end += 1
                    elif annotations[i][0] == "double_peak_top" or annotations[i][0] == "spike-top":
                        # if start != 0 and series[start-1]+s < series[start]:
                        #     start -= 1
                        # start
                        if i != 0:
                            for k in range(annotations[i][1], annotations[i-1][2], -1):
                                if series[k] > series[k-1]+s:
                                    start -= 1
                                else:
                                    break
                        else:
                            for k in range(annotations[i][1], 0, -1):
                                if series[k] > series[k-1]+s/2:
                                    start -= 1
                                else:
                                    break
                        if i != len(annotations)-1:
                            for k in range(annotations[i][2]+1, annotations[i+1][1]):
                                if series[k]+s < series[k-1]:
                                    end += 1
                                else:
                                    break
                        else:
                            for k in range(annotations[i][2]+1, len(series)):
                                if series[k]+s/2 < series[k-1]:
                                    end += 1
                                else:
                                    break
                        # if end+1 < len(series):
                        #     if series[end+1]+s < series[end]:
                        #         end += 1
                    elif annotations[i][0] == "double_peak_bottom" or annotations[i][0] == "spike-bottom":
                        # if start != 0 and series[start-1] > series[start]+s:
                        #     start -= 1

                        # start
                        if i != 0:
                            for k in range(annotations[i][1], annotations[i-1][2], -1):
                                if series[k]+s < series[k-1]:
                                    start -= 1
                                else:
                                    break
                        else:
                            for k in range(annotations[i][1], 0, -1):
                                if series[k]+s/2 < series[k-1]:
                                    start -= 1
                                else:
                                    break
                        if i != len(annotations)-1:
                            for k in range(annotations[i][2]+1, annotations[i+1][1]):
                                if series[k] > series[k-1]+s:
                                    end += 1
                                else:
                                    break
                        else:
                            for k in range(annotations[i][2]+1, len(series)):
                                if series[k] > series[k-1]+s/2:
                                    end += 1
                                else:
                                    break
                        # if end+1 < len(series):
                        #     if series[end+1] > series[end]+s:
                        #         end += 1

                    if len(annotations) == 1:
                        annotations[i][1] = start
                        annotations[i][2] = end
                    else:
                        if i == 0:
                            annotations[i][1] = start
                            if annotations[i][2] <= annotations[i+1][1]:
                                annotations[i][2] = end
                        elif i == len(annotations)-1:
                            if annotations[i][1] >= annotations[i-1][2]:
                                annotations[i][1] = start
                            annotations[i][2] = end
                        else:
                            if annotations[i][1] >= annotations[i-1][2]:
                                annotations[i][1] = start
                            if annotations[i][2] <= annotations[i+1][1]:
                                annotations[i][2] = end

                annotations = merge_tuples(annotations)

                segmentation = []
                categorization = {"input": [], "output": []}
                res_V2 = []
                res_V3 = []
                res_V4 = []
                res_V5 = []
                for annotation in annotations:
                    res_V2.append([annotation[0]] +
                                  list(range(annotation[1], annotation[2]+1)))
                    res_V3.append([annotation[0]] +
                                  list(series[annotation[1]:annotation[2]+1]))
                    index_list = list(range(annotation[1], annotation[2]+1))
                    sampled_elements = random.sample(
                        index_list[1:-1], min(2, len(index_list[1:-1])))
                    sampled_elements.sort()
                    new_index_list = [index_list[0]] + \
                        sampled_elements + [index_list[-1]]
                    value_list = []
                    for i in new_index_list:
                        value_list.append(series[i])
                    # res_V4.append({"p": annotation[0], "idx": new_index_list,"vle":value_list})
                    res_V4.append((annotation[0], new_index_list, value_list))
                    s_list = [series[annotation[1]]]
                    e_list = [series[annotation[2]]]
                    s_index_list = [annotation[1]]
                    e_index_list = [annotation[2]]
                    if 0 <= annotation[1]+1 < len(series):
                        s_index_list.append(annotation[1]+1)
                        s_list.append(series[annotation[1]+1])
                    if 0 <= annotation[1]+2 < len(series):
                        s_index_list.append(annotation[1]+2)
                        s_list.append(series[annotation[1]+2])
                    if 0 <= annotation[2]+1 < len(series):
                        e_index_list.append(annotation[2]+1)
                        e_list.append(series[annotation[2]+1])
                    if 0 <= annotation[2]+2 < len(series):
                        e_index_list.append(annotation[2]+2)
                        e_list.append(series[annotation[2]+2])
                    # res_V5.append({"p": annotation[0], "s_idx": annotation[1], "s_vle": series[annotation[1]], "s_c": s_index_list, "s_m": round(np.mean(s_list),3), "s_std": round(np.std(s_list),3),
                    #              "e_idx": annotation[2], "e_vle": series[annotation[2]], "e_c": e_index_list, "e_m": round(np.mean(e_list),3), "e_std": round(np.std(e_list),3)})
                    # res_V5.append({"p": annotation[0], "s_i": annotation[1], "s_v": series[annotation[1]], "s_m": round(np.mean(s_list),3), "s_std": round(np.std(s_list),3),
                    #               "e_i": annotation[2], "e_v": series[annotation[2]], "e_m": round(np.mean(e_list),3), "e_std": round(np.std(e_list),3)})
                    res_V5.append((annotation[0], annotation[1], annotation[2], series[annotation[1]], series[annotation[2]], round(
                        np.mean(s_list), 3), round(np.std(s_list), 3), round(np.mean(e_list), 3), round(np.std(e_list), 3)))
                    segmentation.append(
                        list(range(annotation[1], annotation[2]+1)))
                    categorization["input"].append(
                        list(series[annotation[1]:annotation[2]+1]))
                    categorization["output"].append(annotation[0])
                image_path = 'F:/line_images/'
                # Plot the series and mark the patterns
                plt.figure(figsize=(14, 5))
                plt.plot(series, label='Time Series')
                for pattern, start, end in annotations:
                    plt.axvspan(start, end, color='red',
                                alpha=0.3, label=pattern+":"+str(start)+"-"+str(end))
                plt.legend()
                plt.savefig(image_path+str(id)+".png")
                plt.close()
                prompts = "时序模式类型=#'trend_up': 一条整体向上倾斜的直线或曲线#,#'trend_down': 一条整体向下倾斜的直线或曲线#,#'cyclic': 一系列的波峰和波谷#,#'spike-top': 一个突出的尖顶#,#'spike-bottom': 一个突出的尖底#,#'double_peak_top': 两个相连的山峰#,#'double_peak_bottom': 两个相连的谷底#。数据如下="

                dataset_1.append({"id": str(id), "conversations": [{"from": "user", "value": prompts+','.join(map(str, series))}, {
                    "from": "assistant", "value": str(annotations)}]})
                dataset_2.append({"id": str(id), "conversations": [{"from": "user", "value": ','.join(map(str, series))}, {
                    "from": "assistant", "value": str(annotations)}]})

                dataset_segmentation.append({"id": str(id), "conversations": [{"from": "user", "value": ','.join(map(str, series))}, {
                    "from": "assistant", "value": str(segmentation)}]})

                for i in range(len(categorization["input"])):
                    dataset_categorization.append({"id": str(id), "conversations": [{"from": "user", "value": ','.join(map(str, categorization["input"][i]))}, {
                        "from": "assistant", "value": categorization["output"][i]}]})

                dataset_V2.append({"id": str(id), "conversations": [{"from": "user", "value": ','.join(map(str, series))}, {
                    "from": "assistant", "value": str(res_V2)}]})

                dataset_V3.append({"id": str(id), "conversations": [{"from": "user", "value": '['+','.join(map(str, series))+']'}, {
                    "from": "assistant", "value": str(res_V3)}]})

                dataset_V4.append({"id": str(id), "conversations": [{"from": "user", "value": '['+','.join(map(str, series))+']'}, {
                    "from": "assistant", "value": str(res_V4)}]})

                dataset_V5.append({"id": str(id), "conversations": [{"from": "user", "value": '['+','.join(map(str, series))+']'}, {
                    "from": "assistant", "value": str(res_V5)}]})

                random.shuffle(dataset_1)
                random.shuffle(dataset_2)
                random.shuffle(dataset_V2)
                random.shuffle(dataset_V3)
                random.shuffle(dataset_V4)
                random.shuffle(dataset_V5)
                random.shuffle(dataset_segmentation)
                random.shuffle(dataset_categorization)

    print(len(dataset_2))
    # # 指定要保存的文件路径
    # file_path_1 = './linedata/dataset_with_prompt_train_10000.json'

    # # 写入JSON数据到文件
    # with open(file_path_1, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_1, file, ensure_ascii=False, indent=4)

    # 指定要保存的文件路径
    # file_path_2 = './linedata/dataset_no_prompt_340_seq_length_10k_samples_v1_train.json'

    # # 写入JSON数据到文件
    # with open(file_path_2, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_2, file, ensure_ascii=False, indent=4)

    # file_path_3 = './linedata/dataset_no_prompt_340_seq_length_10k_samples_segmentation_test.json'

    # # 写入JSON数据到文件
    # with open(file_path_3, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_segmentation, file, ensure_ascii=False, indent=4)

    # file_path_4 = './linedata/dataset_no_prompt_340_seq_length_10k_samples_categorization_test.json'

    # # 写入JSON数据到文件
    # with open(file_path_4, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_categorization, file, ensure_ascii=False, indent=4)

    # file_path_5 = './linedata/dataset_no_prompt_340_seq_length_10k_samples_v2_test.json'

    # # 写入JSON数据到文件
    # with open(file_path_5, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_V2, file, ensure_ascii=False, indent=4)

    # file_path_6 = './linedata/dataset_no_prompt_340_seq_length_10k_samples_v3_test.json'

    # # 写入JSON数据到文件
    # with open(file_path_6, 'w', encoding='utf-8') as file:
    #     json.dump(dataset_V3, file, ensure_ascii=False, indent=4)

    file_path_7 = './linedata/dataset_no_prompt_100_seq_length_5k_samples_v4_test.json'

    # 写入JSON数据到文件
    with open(file_path_7, 'w', encoding='utf-8') as file:
        json.dump(dataset_V4, file, ensure_ascii=False, indent=4)

    file_path_8 = './linedata/dataset_no_prompt_100_seq_length_5k_samples_v5_test.json'

    # 写入JSON数据到文件
    with open(file_path_8, 'w', encoding='utf-8') as file:
        json.dump(dataset_V5, file, ensure_ascii=False, indent=4)


def merge_tuples(arr):
    if not arr:  # 如果输入列表为空，直接返回
        return []

    merged = [arr[0]]  # 初始化合并后的列表，先放入第一个元组
    last_first_value = arr[0][0]  # 记录上一个元组的第一个值
    last_third_value = arr[0][2]  # 记录上一个元组的第三个值

    for i in range(1, len(arr)):
        current = arr[i]
        # 检查当前元组的第一个值是否与上一个相同
        # 且上一个元组的第三个值是否与当前元组的第二个值相同
        if current[0] == last_first_value and last_third_value == current[1] and current[0] in ["trend_down", "trend_up"]:
            # 如果满足条件，合并元组（更新最后一个元组的第三个值）
            merged[-1] = (merged[-1][0], merged[-1][1], current[2])
        else:
            # 不满足合并条件，将当前元组添加到合并后的列表中
            merged.append(current)
            last_first_value = current[0]  # 更新记录的上一个元组的第一个值
        last_third_value = current[2]  # 更新记录的上一个元组的第三个值

    return merged


if __name__ == "__main__":
    main()
