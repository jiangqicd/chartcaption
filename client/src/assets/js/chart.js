//selectedChart表示主视图中的焦点图表，包含了其中数据字段、视觉编码等信息
// const selectedChart = {
//     description: "Here's a chart used to describe timing data patterns",
//     table: { name: '', data: [] },
//     x: { name: '', data: [], operation: '' },
//     y: { name: '', data: [], operation: '' },
//     filter: { selectedAttribute: '', selectedAttributeData: [], type: '', values: [] },
//     saliencyScore: [],
//     visualSaliencyFeature: [],
//     annotations: []
// };

// const selectedChart = {}

// tableData 存储了表格数据，包含属性的详细数值及其类型的映射（例如，数值类、时间类、类别类）
// tableData会在获取到上传表格后自动初始化
// -----------------------------以下是一个案例----------------------------
// tableData = {
//   "GDP": {"type": "numerical", "data": [1,2,3,...]},
//   "Year": {"type": "temporal", "data": [1991,1992,1993,...]},
//   "Country": {"type": "categorical", "data": ["China","USA","UK",...]},
//   ...
// }
// const tableData = {}

// chart.js
import { reactive } from 'vue';

const selectedChart = reactive({});
const tableData = reactive({});

export { selectedChart, tableData }
