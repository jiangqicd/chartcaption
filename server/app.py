import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from pandas.api.types import is_numeric_dtype

from utils.condition import time_keywords
from utils.selectedChart import selectedChart

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


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

        result = {"map_attr_type": map_attr_type,
                  "tableRecords": table.to_json(orient='records'),
                  "selectedChart": selectedchart}

        print(selectedchart)
        return jsonify(result)
    else:
        return jsonify({"error": "File not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
