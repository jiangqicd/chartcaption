<template>
    <div class="col-md-10 plotarea" v-if="isRendered">
        <div>
            <div class="inline-div" style="
            margin-bottom: 3px;
            margin-top: 3px;
            border-bottom: 2px solid gray;
            border-top: 2px solid gray;
          ">
                <div class="badge text-primary-emphasis text-wrap">
                    Annotation view
                </div>
            </div>
            <div style="display: flex;flex-wrap: wrap;">
                <div id="annotationarea">
                </div>
            </div>
            <context-menu></context-menu>
        </div>
    </div>
</template>

<script>
import { inject, ref, watch, nextTick, reactive } from "vue";
import * as d3 from "d3";
// import { add_text_annotations } from '../assets/js/add_text_annotation';
import { highlight_pattern_segment } from '../assets/js/highlight_pattern_segment_v1';
import { update_highlight_pattern_segment } from '../assets/js/update_highlight_pattern_segment';
// import { saveSvgAsPng } from 'svg-to-png';
// import { annotation } from 'd3-svg-annotation';
import { toPng } from 'html-to-image';
export default {
    name: "NavigationBar",
    setup() {

        const annotatedChart = inject("annotatedChart");
        var annotatedChartList = inject("annotatedChartList");

        const isRendered = ref(false)

        // 当数据变化时，确保DOM更新后执行绘图逻辑
        watch(annotatedChartList, (newVal) => {
            // console.log(JSON.parse(annotatedChartList["YearDALY"]["line_patterns_with_annotations"][0]["annotations"]["detail_annotation"]["data_details"]))
            if (Object.keys(newVal).length == 0) {
                const divElement = document.getElementById('annotationarea');
                divElement.innerHTML = "";
            }
            // console.log(annotatedChartList)
            isRendered.value = true
            //newVal.forEach((annotatedChart, index) => {
            Object.keys(newVal).forEach((key, index) => {
                const annotatedChart = newVal[key]
                nextTick(() => {
                    const divElement = document.getElementById('annotationarea');

                    var chartElement = divElement.querySelector('#' + key);

                    console.log("------------")
                    console.log(annotatedChart)

                    if (divElement && !chartElement) {

                        // 创建外部容器
                        const containerDiv = document.createElement('div');
                        containerDiv.id = key; // 设置外部容器的 ID 为 key
                        containerDiv.style.display = 'flex';
                        containerDiv.style.flexDirection = 'column';
                        containerDiv.style.alignItems = 'center'; // 内容居中
                        containerDiv.style.padding = '0';
                        containerDiv.style.margin = '0';
                        containerDiv.style.border = '2px solid gray';

                        // 创建按钮容器
                        const buttonDiv = document.createElement('div');
                        buttonDiv.style.width = '100%'; // 按钮容器宽度与外部容器相同
                        buttonDiv.style.display = 'flex';
                        buttonDiv.style.flexDirection = 'row'; // 按钮排列方式为行
                        buttonDiv.style.justifyContent = 'flex-start'; // 按钮靠左对齐
                        buttonDiv.style.margin = '0';
                        // buttonDiv.style.justifyContent = 'space-around'; // 按钮平均分布

                        // 创建并添加按钮
                        annotatedChart.line_patterns_with_annotations.forEach((p, i) => {

                            // 创建外层子容器div
                            const subContainer = document.createElement('div');
                            subContainer.style.display = 'flex';
                            subContainer.style.alignItems = 'center'; // 垂直居中对齐
                            subContainer.style.paddingLeft = '8px'; // 设置一些外边距
                            subContainer.style.paddingRight = '10px'; // 设置一些外边距 
                            subContainer.style.marginBottom = '1px'; // 设置一些外边距
                            subContainer.style.marginLeft = '1px'; // 设置一些外边距
                            // 设置左右边框
                            // subContainer.style.borderLeft = '2px solid gray'; // 左边框
                            // subContainer.style.borderRight = '2px solid gray'; // 右边框

                            // 添加圆角矩形底色和透明度
                            subContainer.style.borderRadius = '8px'; // 设置圆角大小
                            subContainer.style.backgroundColor = 'rgba(0, 0, 0, 0.1)'; // 设置底色和透明度
                            subContainer.style.opacity = '1'; // 确保透明度不会影响子元素的可见性

                            let d = JSON.parse(annotatedChart.table.data.form_of_records)
                            let x_name = annotatedChart.x.name

                            // 创建带颜色的文本信息
                            const infoText = document.createElement('span');
                            if (i != annotatedChart.line_patterns_with_annotations.length - 1) {
                                infoText.textContent = p.pattern + " : " + d[p.start][x_name] + " -> " + d[p.end][x_name]; // 假设每个pattern有description属性
                                infoText.style.color = "green"; // 使用pattern对象的color属性
                                infoText.style.marginRight = '10px'; // 文本和切换按钮之间的间隔
                            } else {
                                infoText.textContent = p.pattern; // 假设每个pattern有description属性
                                infoText.style.color = "green"; // 使用pattern对象的color属性
                                infoText.style.marginRight = '10px'; // 文本和切换按钮之间的间隔
                            }

                            // 创建标签和切换按钮
                            const toggleLabel = document.createElement('label');
                            toggleLabel.className = 'toggle-btn';
                            // 创建复选框，并设置为选中状态
                            const inputCheckbox = document.createElement('input');
                            inputCheckbox.type = 'checkbox';
                            inputCheckbox.id = "svg_index_" + index + "_" + p.pattern + "_" + p.start + "_" + p.end; // 添加id
                            inputCheckbox.checked = true;
                            // 创建用于显示切换效果的圆形元素
                            const spanCircle = document.createElement('span');
                            spanCircle.className = 'circle';
                            // 将复选框和圆形元素添加到标签中
                            toggleLabel.appendChild(inputCheckbox);
                            toggleLabel.appendChild(spanCircle);

                            // 将文本信息和标签添加到外层子容器div中
                            subContainer.appendChild(infoText);
                            subContainer.appendChild(toggleLabel);

                            // 将整个子容器div添加到之前创建的按钮容器中
                            buttonDiv.appendChild(subContainer);
                        });

                        const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                        // 应用样式
                        svgElement.id = "vis" + key
                        svgElement.style.position = 'relative';
                        // svgElement.style.marginLeft = '10px';
                        svgElement.style.marginTop = '2px';
                        svgElement.style.display = 'flex';
                        svgElement.style.justifyContent = 'center';
                        svgElement.style.alignItems = 'center';
                        svgElement.style.userSelect = 'none';
                        svgElement.style.borderTop = '2px solid gray';

                        // // 添加鼠标移入事件监听器
                        // svgElement.addEventListener('mouseenter', () => {
                        //   // 移除所有 SVG 的光晕效果
                        //   const allSvgElements = divElement.querySelectorAll('svg');
                        //   allSvgElements.forEach(svg => {
                        //     d3.select(svg).selectAll('.halation').remove();
                        //   });

                        //   // 给当前鼠标所在的 SVG 添加光晕效果
                        //   const svg = d3.select(svgElement);
                        //   addGlowEffect(svg);
                        // });

                        // 将 SVG 元素添加到 div 中
                        // 将按钮容器和 SVG 添加到外部容器
                        containerDiv.appendChild(buttonDiv);
                        containerDiv.appendChild(svgElement);

                        // 将外部容器添加到原始 div 中
                        divElement.appendChild(containerDiv);
                        // drawLineChart(`#annotation-${index.toString()}`, annotatedChart, index);
                        drawLineChart("#vis" + key, annotatedChart, index);
                    }
                });
            });
        });

        // 添加光晕效果的函数
        // const addGlowEffect = (svg) => {
        //   // 添加一个定义过滤器的<defs>元素
        //   const defs = svg.append("defs");

        //   // 在<defs>中添加一个<filter>元素，并设置其ID
        //   const filter = defs.append("filter")
        //     .attr("id", "focus")
        //     .attr("x", "-200%")
        //     .attr("y", "-200%")
        //     .attr("width", "400%")
        //     .attr("height", "400%");

        //   // 在<filter>中添加一个<feGaussianBlur>元素来创建模糊效果
        //   filter.append("feGaussianBlur")
        //     .attr("stdDeviation", "2.5") // 模糊程度
        //     .attr("result", "coloredBlur");

        //   // 添加一个<feMerge>元素来合并效果
        //   const feMerge = filter.append("feMerge");

        //   // 将模糊效果和原始图形合并
        //   feMerge.append("feMergeNode")
        //     .attr("in", "coloredBlur");

        //   feMerge.append("feMergeNode")
        //     .attr("in", "SourceGraphic");
        //   ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]
        //   // 给 SVG 添加一个矩形作为边框
        //   svg.append('rect')
        //     .attr("class", "halation")
        //     .attr('x', 0)
        //     .attr('y', 0)
        //     .attr('width', '100%')
        //     .attr('height', '100%')
        //     .attr('fill', 'none')
        //     .attr('stroke', "green")
        //     .attr('stroke-width', '4px')
        //     .attr('filter', 'url(#focus)');

        // };

        function drawLineChart(element, annotatedChart, index) {

            const width = 1560; // 图表的宽度
            const height = 820; // 图表的高度
            const margin = { top: 20, right: 20, bottom: 30, left: 70 };


            // 创建SVG容器
            const svg = d3
                .select(element)
                .attr("width", width)
                .attr("height", height);

            // 首先，清空 SVG 容器中的所有内容
            d3.select(element).selectAll("*").remove();

            //tag_text用来呈现图表中的过滤信息
            let tag_text = ""

            if (annotatedChart["filter"]["selectedAttribute"] != "" && annotatedChart["filter"]["values"] != "") {
                if (annotatedChart["filter"]["type"] == "oneOf") {
                    tag_text = annotatedChart["filter"]["selectedAttribute"] + " = " + annotatedChart["filter"]["values"][0]
                } else {
                    tag_text = annotatedChart["filter"]["selectedAttribute"] + " : from " + annotatedChart["filter"]["values"][0] + " to " + annotatedChart["filter"]["values"][1]
                }
                const tag = svg.append("text")
                    .text(tag_text)
                    .attr("x", margin.left - 20)
                    .attr("y", margin.top - 3)
                    .attr("text-anchor", "middle")
                    .style("fill", "white")
                    .style("font-size", "11px")

                var bbox = {}
                if (tag.node() !== null) {
                    // 元素已被渲染
                    bbox = tag.node().getBBox();
                    // 执行其他操作
                }


                svg.insert("rect", "text")
                    .attr("x", bbox.x - 5)
                    .attr("y", bbox.y - 5)
                    .attr("width", bbox.width + 10)
                    .attr("height", bbox.height + 10)
                    .attr("fill", "gray")
                    // .attr("stroke", "gray")
                    .attr("rx", 5)
                    .attr("ry", 5);
            }

            const remove_img = svg.append('image')
                .attr('x', width - 60)
                .attr('height', 0)
                .attr('width', 20)
                .attr('height', 20)
                .style('opacity', 0.7)
                .style('cursor', 'pointer')
                .attr('href', '/icons/remove.png')
                .on('mouseover', function () {
                    d3.select(this).style('opacity', 1);
                })
                .on('mouseout', function () {
                    d3.select(this).style('opacity', 0.7);
                })
                .on('click', function () {
                    // 获取SVG元素的父级div元素
                    const parentDiv = svg.node().parentNode;

                    // 删除该div元素
                    parentDiv.remove();
                    delete annotatedChartList[element.replace('#', '')];
                    // annotatedChartList.splice(parseInt(element.replace('#annotation-', '')), 1)
                });

            remove_img.raise()

            const export_img = svg.append('image')
                .attr('x', width - 35)
                .attr('height', 0)
                .attr('width', 20)
                .attr('height', 20)
                .style('opacity', 0.7)
                .style('cursor', 'pointer')
                .attr('href', '/icons/export.png')
                .on('mouseover', function () {
                    d3.select(this).style('opacity', 1);
                })
                .on('mouseout', function () {
                    d3.select(this).style('opacity', 0.7);
                })
                .on('click', function () {
                    exportSvg()
                });

            const exportSvg = async () => {
                try {
                    // 获取 SVG 的尺寸
                    const svgWidth = svg.node().clientWidth;
                    const svgHeight = svg.node().clientHeight;

                    // 创建 SVG 的深拷贝
                    const svgCopy = svg.node().cloneNode(true);
                    d3.select(svgCopy).selectAll('image').remove();
                    d3.select(svgCopy).select('rect').remove();
                    d3.select(svgCopy).select('.halation').remove();
                    d3.select(svgCopy).style('border', 'none');

                    // 将修改后的 SVG 转换为 PNG
                    const dataUrl = await toPng(svgCopy, {
                        width: svgWidth + 40,
                        height: svgHeight + 40,
                        backgroundColor: 'white',
                    });

                    // 创建下载链接并触发下载
                    const link = document.createElement('a');
                    link.href = dataUrl;
                    link.download = 'exported_image.png';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } catch (error) {
                    console.error('导出失败:', error);
                }
            };
            export_img.raise()

            const selectedXValue = ref("");
            const selectedYValue = ref("");
            const selectedXOperation = ref("");
            const selectedYOperation = ref("");

            selectedXValue.value = annotatedChart.x.name;
            selectedYValue.value = annotatedChart.y.name;
            selectedXOperation.value = annotatedChart.x.operation;
            selectedYOperation.value = annotatedChart.y.operation;

            //------------------------数据预处理---------------------------------//

            var data = JSON.parse(annotatedChart.table.data.form_of_records);

            const rawdata = [...data]

            const detail_data = [];

            const correlation_attr_data = [];

            const correlation_obj_data = [];

            const lag_attr_data = [];

            const lag_obj_data = [];

            for (let i = 0; i < annotatedChart["line_patterns_with_annotations"].length - 1; i++) {

                const detail_attrs = []
                let annotations = annotatedChart["line_patterns_with_annotations"][i]["annotations"]

                //获取detail_annotation数据
                if ("detail_annotation" in annotations) {
                    let detail_sub_data = JSON.parse(annotations["detail_annotation"]["data_details"]);
                    Object.keys(detail_sub_data[0]).forEach(key => {
                        if (key != selectedXValue.value && key != selectedYValue.value) {
                            detail_attrs.push(key)
                        }
                    });
                    detail_sub_data.forEach(item_i => {
                        rawdata.forEach(item_j => {
                            if (item_i[selectedXValue.value] == item_j[selectedXValue.value]) {
                                item_i["index"] = item_j["index"]
                            }
                        })
                    })
                    let rollupData = null
                    if (selectedYOperation.value == "null" || selectedYOperation.value == "mean") {
                        rollupData = d3.rollup(detail_sub_data,
                            v => d3.mean(v, d => d[selectedYValue.value]), // 计算每个组内的 GDP 平均值
                            d => d[selectedXValue.value], // 第一层分组按年份
                            d => d[detail_attrs[0]] // 第二层分组按国家
                        )
                    } else if (selectedYOperation.value == "sum") {
                        rollupData = d3.rollup(detail_sub_data,
                            v => d3.sum(v, d => d[selectedYValue.value]), // 计算每个组内的 GDP 平均值
                            d => d[selectedXValue.value], // 第一层分组按年份
                            d => d[detail_attrs[0]] // 第二层分组按国家
                        )
                    } else if (selectedYOperation.value == "min") {
                        rollupData = d3.rollup(detail_sub_data,
                            v => d3.min(v, d => d[selectedYValue.value]), // 计算每个组内的 GDP 平均值
                            d => d[selectedXValue.value], // 第一层分组按年份
                            d => d[detail_attrs[0]] // 第二层分组按国家
                        )
                    } else if (selectedYOperation.value == "max") {
                        rollupData = d3.rollup(detail_sub_data,
                            v => d3.max(v, d => d[selectedYValue.value]), // 计算每个组内的 GDP 平均值
                            d => d[selectedXValue.value], // 第一层分组按年份
                            d => d[detail_attrs[0]] // 第二层分组按国家
                        )
                    }
                    let detail_data_final = Array.from(rollupData, ([key1, value]) =>
                        Array.from(value, ([key2, meanValue]) => ({
                            [selectedXValue.value]: key1,
                            [detail_attrs[0]]: key2,
                            [selectedYValue.value]: meanValue
                        }))
                    ).flat();

                    detail_data_final.forEach(item_i => {
                        rawdata.forEach(item_j => {
                            if (item_i[selectedXValue.value] == item_j[selectedXValue.value]) {
                                item_i["index"] = item_j["index"]
                            }
                        })
                    })
                    detail_data.push(...detail_data_final)

                    //获取correlation_annotation数据

                    if ("correlation_annotation" in annotations) {
                        let data_filter_context = annotatedChart.table.data.data_filter_context
                        annotations["correlation_annotation"]["obj_obj"].forEach((element) => {

                            let obj_data = data_filter_context[element["attr"]]

                            obj_data.forEach((e, i) => {
                                if (i >= parseInt(element["start"]) && i <= parseInt(element["end"])) {
                                    correlation_obj_data.push({
                                        "index": rawdata[i]["index"],
                                        [selectedXValue.value]: rawdata[i][selectedXValue.value],
                                        [selectedYValue.value]: e,
                                        "corr": element["corr"]
                                    })
                                }
                            })


                        })

                        let attr_data = {}

                        annotations["correlation_annotation"]["attr_attr"].forEach((element) => {
                            attr_data[element["attr"]] = []
                            rawdata.forEach((e, i) => {
                                if (i >= parseInt(element["start"]) && i <= parseInt(element["end"])) {
                                    attr_data[element["attr"]].push({
                                        [selectedXValue.value]: rawdata[i][selectedXValue.value],
                                        [element["attr"]]: rawdata[i][element["attr"]],
                                        "index": rawdata[i]["index"],
                                        "corr": element["corr"]
                                    })
                                }
                            })
                        })

                        correlation_attr_data.push(attr_data)
                    }

                    //获取lag_annotation数据

                    if ("lag_annotation" in annotations) {
                        let data_filter_context = annotatedChart.table.data.data_filter_context
                        annotations["lag_annotation"]["obj_obj"].forEach((element) => {

                            let obj_data = data_filter_context[element["attr"]]

                            obj_data.forEach((e, i) => {
                                if (i >= parseInt(element["start"]) && i <= parseInt(element["end"])) {
                                    lag_obj_data.push({
                                        "index": rawdata[i]["index"],
                                        [selectedXValue.value]: rawdata[i][selectedXValue.value],
                                        [selectedYValue.value]: e,
                                        "corr": element["corr"]
                                    })
                                }
                            })


                        })

                        let attr_data = {}

                        annotations["lag_annotation"]["attr_attr"].forEach((element) => {
                            attr_data[element["attr"]] = []
                            rawdata.forEach((e, i) => {
                                if (i >= parseInt(element["start"]) && i <= parseInt(element["end"])) {
                                    attr_data[element["attr"]].push({
                                        [selectedXValue.value]: rawdata[i][selectedXValue.value],
                                        [element["attr"]]: rawdata[i][element["attr"]],
                                        "index": rawdata[i]["index"],
                                        "corr": element["corr"]
                                    })
                                }
                            })
                        })

                        lag_attr_data.push(attr_data)
                    }
                }
            }

            console.log(detail_data)

            const prediction_start_index = data.length


            // 设置x轴的比例尺，现在它将基于数据点的索引
            console.log(rawdata)

            data.pop()
            console.log(prediction_start_index)

            const prediction_data = JSON.parse(annotatedChart.annotations.prediction_annotation[0]["prediction_data"])
            const prediction_upper = JSON.parse(annotatedChart.annotations.prediction_annotation[0]["prediction_upper"])
            const prediction_lower = JSON.parse(annotatedChart.annotations.prediction_annotation[0]["prediction_lower"])
            const prediction_label = annotatedChart.annotations.prediction_annotation[0]["x_data"]

            for (let i = 0; i < prediction_label.length; i++) {
                data.push({ "index": data.length, [selectedYValue.value]: prediction_data[i], "up": prediction_upper[i], "low": prediction_lower[i], [selectedXValue.value]: prediction_label[i] })
            }


            console.log("+++++++++++++++++++++++++++++++")
            console.log(data)

            const selectedXData = reactive([])
            const selectedYData = reactive([])//数组
            const selectedDetailsData = reactive([])//数组
            const selectedCorrelationAttrData = reactive([])
            const selectedLagAttrData = reactive([])
            const selectedCorrelationObjData = reactive([])
            const selectedLagObjData = reactive([])

            selectedXData.splice(0, selectedXData.length, ...data);
            selectedYData.splice(0, selectedYData.length, ...data);
            selectedDetailsData.splice(0, selectedDetailsData.length, ...detail_data);
            selectedCorrelationAttrData.splice(0, selectedCorrelationAttrData.length, ...correlation_attr_data);
            selectedCorrelationObjData.splice(0, selectedCorrelationObjData.length, ...correlation_obj_data);
            selectedLagAttrData.splice(0, selectedLagAttrData.length, ...lag_attr_data);
            selectedLagObjData.splice(0, selectedLagObjData.length, ...lag_obj_data);

            //=================================================================================================

            //存储了每个图表所有具体注释段的开启关闭状态
            const isAnnotationsEnabled = reactive([]);

            annotatedChart.line_patterns_with_annotations.forEach(() => {
                isAnnotationsEnabled.push(true)
            })

            const isTextAnnotationEnableList = reactive([])
            const isDetailsEnableList = reactive([])
            const selectedDetailsAttrList = reactive([])

            // //存储了不同注释内容的状态
            // const detailVars = reactive([]);
            // const correlationVars = reactive([]);
            // const lagVars = reactive([]);

            // watch(detailVars, () => {
            //     // 检查所有变量是否都为1
            //     let allAreOne = detailVars.every(v => v.value === false);
            //     isDetail.value = !allAreOne;
            //     console.log(detailVars)
            //     console.log(`reactiveVar isDetail changed to ${isDetail.value}`);
            // });

            // watch(correlationVars, () => {
            //     // 检查所有变量是否都为1
            //     let allAreOne = correlationVars.every(v => v.value === false);
            //     isCorrelation.value = !allAreOne;
            //     console.log(correlationVars)
            //     console.log(`reactiveVar isCorrelation changed to ${isCorrelation.value}`);
            // });

            // watch(lagVars, () => {
            //     // 检查所有变量是否都为1
            //     let allAreOne = lagVars.every(v => v.value === false);
            //     isLag.value = !allAreOne;
            //     console.log(lagVars)
            //     console.log(`reactiveVar isLag changed to ${isLag.value}`);
            // })

            // //存储了不同注释内容的状态
            // const isDetail = ref(true);
            // const isCorrelation = ref(true);
            // const isLag = ref(true);
            // const isPrediction = ref(true);

            annotatedChart.line_patterns_with_annotations.forEach((p, i) => {
                const checkbox = document.getElementById("svg_index_" + index + "_" + p.pattern + "_" + p.start + "_" + p.end);
                checkbox.addEventListener('change', function () {
                    isAnnotationsEnabled[i] = this.checked
                });
            })

            render(svg, selectedXData, selectedYData, selectedDetailsData, selectedCorrelationAttrData, selectedCorrelationObjData, selectedLagAttrData, selectedLagObjData)

            watch([selectedXData, selectedYData, selectedDetailsData, selectedCorrelationObjData, selectedLagObjData], ([newselectedXData, newselectedYData, newselectedDetailsData, newselectedCorrelationObjData, newselectedLagObjData]) => {
                console.log("*************发生改变****************")
                console.log(newselectedXData, newselectedYData, newselectedDetailsData, selectedCorrelationAttrData, newselectedCorrelationObjData, selectedLagAttrData, newselectedLagObjData)
                annotatedChart["line_patterns_with_annotations"].forEach((annotations) => {
                    let contentToToggle = d3.selectAll("#svg_index_" + index + "_" + annotations["pattern"] + "_" + annotations["start"] + "_" + annotations["end"] + "_vis");
                    if (contentToToggle) { contentToToggle.remove() }
                    let contentToToggleText = d3.selectAll("#svg_index_" + index + "_" + "textannotation" + annotations["start"] + annotations["end"]);
                    if (contentToToggleText) { contentToToggleText.remove() }
                    let contentToToggleDetails = d3.selectAll("#svg_index_" + index + "_details_" + annotations["start"] + "_" + annotations["end"] + "_vis");
                    if (contentToToggleDetails) { contentToToggleDetails.remove() }
                })
                update(svg, newselectedXData, newselectedYData, newselectedDetailsData, selectedCorrelationAttrData, newselectedCorrelationObjData, selectedLagAttrData, newselectedLagObjData)
            })

            function render(svg, selectedXData, selectedYData, selectedDetailsData, selectedCorrelationAttrData, selectedCorrelationObjData, selectedLagAttrData, selectedLagObjData) {
                // console.log(selectedXData, selectedYData, selectedDetailsData, selectedCorrelationAttrData, selectedCorrelationObjData, selectedLagAttrData, selectedLagObjData)
                const xScale = d3
                    .scaleLinear()
                    .domain([d3.min(selectedXData, (d) => d["index"]), d3.max(selectedXData, (d) => d["index"])]) // 数据点索引的范围从0到data.length-1
                    .range([margin.left, width - margin.right]);

                const y_min_original = d3.min(selectedYData, (d) => d[selectedYValue.value])

                const y_max_original = d3.max(selectedYData, (d) => d[selectedYValue.value])

                const y_min_prediction = d3.min(selectedYData, (d) => d["low"]) || Infinity

                const y_max_prediction = d3.max(selectedYData, (d) => d["up"]) || -Infinity

                const y_min_details = d3.min(selectedDetailsData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_details = d3.max(selectedDetailsData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min_correlation = d3.min(selectedCorrelationObjData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_correlation = d3.max(selectedCorrelationObjData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min_lag = d3.min(selectedLagObjData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_lag = d3.max(selectedLagObjData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min = Math.min(y_min_original, y_min_prediction, y_min_details, y_min_correlation, y_min_lag)

                const y_max = Math.max(y_max_original, y_max_prediction, y_max_details, y_max_correlation, y_max_lag)

                const yScale = d3
                    .scaleLinear()
                    .domain([y_min - 0.1 * (y_max - y_min), y_max + 0.1 * (y_max - y_min)]) // d.y是你的数据中y轴的值
                    .range([height - margin.bottom, margin.top]);

                let line = d3
                    .line()
                    .x((d) => xScale(d["index"]))
                    .y((d) => yScale(d[selectedYValue.value]));

                // 添加x轴
                svg.append("g")
                    .attr("id", "x-axis" + index)
                    .attr("transform", `translate(0,${height - margin.bottom})`)
                    .call(
                        d3.axisBottom(xScale)
                            .ticks(data.length)  // 确保刻度数量与数据长度一致
                            .tickFormat((d, i) => {
                                const interval = 3;  // 设置显示间隔，例如每隔5个显示一次
                                if (i % interval === 0) {
                                    return data[i][selectedXValue.value];
                                } else {
                                    return "";  // 其他情况下返回空字符串，不显示刻度标签
                                }
                            })
                    );

                // 添加y轴
                svg
                    .append("g")
                    .attr("id", "y-axis" + index)
                    .attr("transform", `translate(${margin.left},0)`)
                    .call(d3.axisLeft(yScale))
                    .select(".domain") // 选择轴线部分
                    .style("stroke", "none"); // 设置轴线颜色为透明


                // 网格线
                svg
                    .selectAll(".grid-line.x" + index)
                    .data(d3.range(data.length))
                    .enter()
                    .append("line")
                    .attr("class", "grid-line-x" + index)
                    .attr("x1", (d, i) => xScale(i))
                    .attr("x2", (d, i) => xScale(i))
                    .attr("y1", margin.top)
                    .attr("y2", height - margin.bottom)
                    .style("stroke", "#ddd")
                    .style("stroke-opacity", 0.7);

                svg
                    .selectAll(".grid-line.y" + index)
                    .data(yScale.ticks(10))
                    .enter()
                    .append("line")
                    .attr("class", "grid-line-y" + index)
                    .attr("x1", margin.left)
                    .attr("x2", width - margin.right)
                    .attr("y1", (d) => yScale(d))
                    .attr("y2", (d) => yScale(d))
                    .style("stroke", "#ddd")
                    .style("stroke-opacity", 0.7);

                // 自定义轴样式
                svg
                    .selectAll(".axis path, .axis line")
                    .style("fill", "none")
                    .style("stroke", "#000")
                    .style("shape-rendering", "crispEdges");

                svg
                    .selectAll(".axis text")
                    .style("font-family", "Arial, sans-serif")
                    .style("font-size", "12px");

                // 添加 x 轴标签
                svg
                    .append("text")
                    .attr("transform", `translate(${width / 2}, ${height + margin.bottom - 35})`) // 将文本定位在 x 轴下方正中央
                    .style("text-anchor", "middle") // 文本居中对齐
                    .style("font-size", "12px")
                    .text(selectedXValue.value); // 替换为你的 x 轴标签文本

                // 添加 y 轴标签
                svg
                    .append("text")
                    .attr(
                        "transform",
                        `rotate(-90) translate(${-height / 2 - margin.top / 2}, ${margin.left - 50})`
                    ) // 旋转并定位文本至 y 轴左侧
                    .style("text-anchor", "middle") // 文本垂直居中对齐
                    .style("font-size", "12px")
                    .text(selectedYValue.value); // 替换为你的 y 轴标签文本

                // 绘制原始数据线段
                svg
                    .append("path")
                    .datum(data.slice(0, prediction_start_index))
                    .attr("fill", "none")
                    .attr("stroke", "steelblue")
                    .attr("stroke-width", 1.5)
                    .attr("id", "original_line" + index)
                    .attr("d", line)

                // 绘制注释内容

                for (let i = 0; i < annotatedChart["line_patterns_with_annotations"].length; i++) {
                    const annotations = annotatedChart["line_patterns_with_annotations"][i]["annotations"]
                    const pattern = annotatedChart["line_patterns_with_annotations"][i]["pattern"]
                    const start = parseInt(annotatedChart["line_patterns_with_annotations"][i]["start"])
                    const end = parseInt(annotatedChart["line_patterns_with_annotations"][i]["end"])
                    const textAnchorPoint = data[Math.floor((start + end) / 2)];
                    const textAnchorX = xScale(Math.floor((start + end) / 2));
                    const textAnchorY = yScale(textAnchorPoint[selectedYValue.value]);
                    const parameters = {
                        "annotatedChart": annotatedChart,
                        "annotationsList": annotatedChart["line_patterns_with_annotations"],
                        "svg_index": index,
                        "container": svg,
                        "annotation_start_index": start,
                        "annotation_end_index": end,
                        "annotations": annotations,
                        "pattern": pattern,
                        "data": data,
                        "textAnchorX": textAnchorX,
                        "textAnchorY": textAnchorY,
                        "x_scale_keyword": "index",
                        "y_scale_keyword": selectedYValue.value,
                        "x_name": selectedXValue.value,
                        "y_name": selectedYValue.value,
                        "prediction_start_index": prediction_start_index,
                        "xScale": xScale,
                        "selectedXScale": xScale,
                        "selectedYScale": yScale,
                        "selectedLineScale": line,
                        "aggregation": selectedYOperation.value,
                        "data_with_prediction": data,
                        "data_without_prediction": rawdata,
                        "selectedXData": selectedXData,
                        "selectedYData": selectedYData,
                        "selectedDetailsData": selectedDetailsData,
                        "selectedCorrelationAttrData": selectedCorrelationAttrData,
                        "selectedCorrelationObjData": selectedCorrelationObjData,
                        "selectedLagAttrData": selectedLagAttrData,
                        "selectedLagObjData": selectedLagObjData,
                        "isTextAnnotationEnableList": isTextAnnotationEnableList,
                        "isDetailsEnableList": isDetailsEnableList,
                        "selectedDetailsAttrList": selectedDetailsAttrList,
                        "isAnnotationsEnabled": isAnnotationsEnabled,
                        "annotation_index": i
                    }

                    highlight_pattern_segment(parameters)

                }
            }

            //更新注释内容
            function update(svg, selectedXData, selectedYData, selectedDetailsData, selectedCorrelationAttrData, selectedCorrelationObjData, selectedLagAttrData, selectedLagObjData) {
                const xScale = d3
                    .scaleLinear()
                    .domain([d3.min(selectedXData, (d) => d["index"]), d3.max(selectedXData, (d) => d["index"])]) // 数据点索引的范围从0到data.length-1
                    .range([margin.left, width - margin.right]);

                const y_min_original = d3.min(selectedYData, (d) => d[selectedYValue.value])

                const y_max_original = d3.max(selectedYData, (d) => d[selectedYValue.value])

                const y_min_prediction = d3.min(selectedYData, (d) => d["low"]) || Infinity

                const y_max_prediction = d3.max(selectedYData, (d) => d["up"]) || -Infinity

                const y_min_details = d3.min(selectedDetailsData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_details = d3.max(selectedDetailsData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min_correlation = d3.min(selectedCorrelationObjData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_correlation = d3.max(selectedCorrelationObjData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min_lag = d3.min(selectedLagObjData, (d) => d[selectedYValue.value]) || Infinity

                const y_max_lag = d3.max(selectedLagObjData, (d) => d[selectedYValue.value]) || -Infinity

                const y_min = Math.min(y_min_original, y_min_prediction, y_min_details, y_min_correlation, y_min_lag)

                const y_max = Math.max(y_max_original, y_max_prediction, y_max_details, y_max_correlation, y_max_lag)

                const yScale = d3
                    .scaleLinear()
                    .domain([y_min - 0.1 * (y_max - y_min), y_max + 0.1 * (y_max - y_min)]) // d.y是你的数据中y轴的值
                    .range([height - margin.bottom, margin.top]);

                let line = d3
                    .line()
                    .x((d) => xScale(d["index"]))
                    .y((d) => yScale(d[selectedYValue.value]));

                d3.select("#original_line" + index)
                    .transition()
                    .duration(1000)
                    .attr("d", line);

                d3.select("#y-axis" + index)
                    .transition()
                    .duration(1000)
                    .call(d3.axisLeft(yScale))
                    .select(".domain")
                    .style("stroke", "none");

                const gridLinesY = svg.selectAll(".grid-line-y" + index)
                    .data(yScale.ticks(10))

                // // 更新现有的网格线
                gridLinesY.transition()
                    .duration(1000) // 设置过渡持续时间为1000毫秒
                    .attr("y1", (d) => yScale(d))
                    .attr("y2", (d) => yScale(d))

                // 添加新的网格线
                gridLinesY.enter()
                    .append("line")
                    .attr("class", "grid-line-y" + index)
                    .attr("x1", margin.left)
                    .attr("x2", width - margin.right)
                    .attr("y1", (d) => yScale(d))
                    .attr("y2", (d) => yScale(d))
                    .style("stroke", "#ddd")
                    .style("stroke-opacity", 0.7);
                // 移除多余的网格线
                gridLinesY.exit().remove();

                d3.select("#x-axis" + index)
                    .attr("transform", `translate(0,${height - margin.bottom})`)
                    .transition()
                    .duration(1000)
                    .call(
                        d3.axisBottom(xScale)
                            .ticks(data.length)  // 确保刻度数量与数据长度一致
                            .tickFormat((d, i) => {
                                const interval = 3;  // 设置显示间隔，例如每隔5个显示一次
                                if (i % interval === 0) {
                                    return data[i][selectedXValue.value];
                                } else {
                                    return "";  // 其他情况下返回空字符串，不显示刻度标签
                                }
                            })
                    );

                const gridLinesX = svg.selectAll(".grid-line-x" + index)
                    .data(d3.range(data.length))

                // // 更新现有的网格线
                gridLinesX.transition()
                    .duration(1000) // 设置过渡持续时间为1000毫秒
                    .attr("x1", (d, i) => xScale(i))
                    .attr("x2", (d, i) => xScale(i))

                // 添加新的网格线
                gridLinesX.enter()
                    .append("line")
                    .attr("class", "grid-line-y" + index)
                    .attr("x1", (d, i) => xScale(i))
                    .attr("x2", (d, i) => xScale(i))
                    .attr("y1", margin.top)
                    .attr("y2", height - margin.bottom)
                    .style("stroke", "#ddd")
                    .style("stroke-opacity", 0.7);
                // 移除多余的网格线
                gridLinesX.exit().remove();

                // 绘制注释内容

                for (let i = 0; i < annotatedChart["line_patterns_with_annotations"].length; i++) {
                    const annotations = annotatedChart["line_patterns_with_annotations"][i]["annotations"]
                    const pattern = annotatedChart["line_patterns_with_annotations"][i]["pattern"]
                    const start = parseInt(annotatedChart["line_patterns_with_annotations"][i]["start"])
                    const end = parseInt(annotatedChart["line_patterns_with_annotations"][i]["end"])
                    const textAnchorPoint = data[Math.floor((start + end) / 2)];
                    const textAnchorX = xScale(Math.floor((start + end) / 2));
                    const textAnchorY = yScale(textAnchorPoint[selectedYValue.value]);
                    const parameters = {
                        "annotatedChart": annotatedChart,
                        "annotationsList": annotatedChart["line_patterns_with_annotations"],
                        "svg_index": index,
                        "container": svg,
                        "annotation_start_index": start,
                        "annotation_end_index": end,
                        "annotations": annotations,
                        "pattern": pattern,
                        "data": data,
                        "textAnchorX": textAnchorX,
                        "textAnchorY": textAnchorY,
                        "x_scale_keyword": "index",
                        "y_scale_keyword": selectedYValue.value,
                        "x_name": selectedXValue.value,
                        "y_name": selectedYValue.value,
                        "prediction_start_index": prediction_start_index,
                        "selectedXScale": xScale,
                        "selectedYScale": yScale,
                        "selectedLineScale": line,
                        "aggregation": selectedYOperation.value,
                        "data_with_prediction": data,
                        "data_without_prediction": rawdata,
                        "selectedXData": selectedXData,
                        "selectedYData": selectedYData,
                        "selectedDetailsData": selectedDetailsData,
                        "selectedCorrelationAttrData": selectedCorrelationAttrData,
                        "selectedCorrelationObjData": selectedCorrelationObjData,
                        "selectedLagAttrData": selectedLagAttrData,
                        "selectedLagObjData": selectedLagObjData,
                        "isTextAnnotationEnableList": isTextAnnotationEnableList,
                        "isDetailsEnableList": isDetailsEnableList,
                        "selectedDetailsAttrList": selectedDetailsAttrList,
                        "isAnnotationsEnabled": isAnnotationsEnabled,
                        "annotation_index": i
                    }

                    update_highlight_pattern_segment(parameters)

                }
            }
        }
        return {
            annotatedChart, isRendered, annotatedChartList
        };
    },
};
</script>

<style>
.plotarea {
    border-right: 2px solid gray;
    height: 900px;
}

.textannotation {
    border-right: 2px solid gray;
}

#annotationarea {
    overflow-y: hidden;
    /* 默认情况下隐藏垂直滚动条 */
    height: 870px;
    width: 100%;
    position: relative;
    display: flex;
    flex-wrap: wrap;
    /* 可以设置一个固定高度,或者使用其他方法来确定高度 */
}

#annotationarea:hover {
    overflow-y: auto;
    /* 当鼠标悬停时显示垂直滚动条 */
}

#annotationarea::-webkit-scrollbar {
    width: 8px;
    /* 设置滚动条宽度 */
}

#annotationarea::-webkit-scrollbar-track {
    background-color: #f1f1f1;
    /* 设置滚动条背景色 */
}

#annotationarea::-webkit-scrollbar-thumb {
    background-color: #cbc7c7;
    /* 设置滚动条滑块颜色 */
    border-radius: 6px;
    /* 设置滑块圆角 */
}

#annotationarea::-webkit-scrollbar-thumb:hover {
    background-color: #cbc7c7;
    /* 设置鼠标悬停时滑块颜色 */
}

*,
::before,
::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    margin-top: 1px;
    /* 设置所有元素的上边距为1px */
}

.toggle-btn {
    width: 80px;
    height: 25px;
    position: relative;
    display: inline-block;
}

.toggle-btn input[type="checkbox"] {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 100vmax;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    cursor: pointer;
    transition: all 150ms ease-in-out;
    outline: none;
    background-color: #cdd0d0;
}

.toggle-btn .circle {
    position: absolute;
    width: 50%;
    height: 100%;
    top: 50%;
    left: 0%;
    transform: translateY(-50%);
    background-color: #7a8b8b;
    transition: all 150ms ease-in-out;
    pointer-events: none;
    border-radius: 80vmax;
    box-shadow: 0 2px 5px #696969;
    margin-top: -1px;
    /* 设置所有元素的上边距为1px */
}

.toggle-btn .circle::before {
    content: "OFF";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-weight: 700;
    color: #f2f3f3;
    font-family: sans-serif;
}

.toggle-btn input[type="checkbox"]:checked {
    background-color: #e2710e;
}

.toggle-btn input[type="checkbox"]:checked~.circle {
    background-color: #f2f3f3;
    left: 50%;
}

.toggle-btn input[type="checkbox"]:checked~.circle::before {
    content: "ON";
    color: #e2710e;
}

.tooltip {
    position: absolute;
    background-color: #fff;
    border: 1px solid #ccc;
    padding: 5px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
    border-radius: 10px;
    /* 圆角设置为10px */
}
</style>