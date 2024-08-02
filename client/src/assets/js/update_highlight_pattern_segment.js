import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
import ContextMenu from '@imengyu/vue3-context-menu'
import { add_text_annotations } from './add_text_annotation';
import { add_prediction_annotation } from './add_prediction_annotation';
import { add_details_annotation } from './add_details_annotation';
// import hide from '@/assets/icons/hide.svg';
import { h, reactive } from "vue"
export function update_highlight_pattern_segment(parameters) {

    // const annotationsList = parameters["annotationsList"]
    const svg = parameters["container"]
    const index = parameters["svg_index"]
    const start = parameters["annotation_start_index"]
    const end = parameters["annotation_end_index"]
    const data = parameters["data"]
    const annotations = parameters["annotations"]
    const pattern = parameters["pattern"]
    // const textAnchorX = parameters["textAnchorX"]
    // const textAnchorY = parameters["textAnchorY"]
    const prediction_start_index = parameters["prediction_start_index"]
    const x_scale_keyword = parameters["x_scale_keyword"]
    const y_scale_keyword = parameters["y_scale_keyword"]
    let xScale = parameters["selectedXScale"]
    let yScale = parameters["selectedYScale"]
    let line = parameters["selectedLineScale"]
    const x_name = parameters["x_name"]
    const y_name = parameters["y_name"]
    const aggregation = parameters["aggregation"]
    const i = parameters["annotation_index"]
    const isAnnotationsEnabled = parameters["isAnnotationsEnabled"]

    const isTextAnnotationEnableList = parameters["isTextAnnotationEnableList"]
    const isDetailsEnableList = parameters["isDetailsEnableList"]
    const selectedDetailsAttrList = parameters["selectedDetailsAttrList"]

    const data_X_Y_with_prediction = parameters["data_with_prediction"]
    const data_X_Y_without_prediction = parameters["data_without_prediction"]
    const selectedXData = parameters["selectedXData"]
    const selectedYData = parameters["selectedYData"]
    const selectedDetailsData = parameters["selectedDetailsData"]
    const selectedCorrelationAttrData = parameters["selectedCorrelationAttrData"]
    const selectedCorrelationObjData = parameters["selectedCorrelationObjData"]
    const selectedLagAttrData = parameters["selectedLagAttrData"]
    const selectedLagObjData = parameters["selectedLagObjData"]

    console.log(data_X_Y_with_prediction, data_X_Y_without_prediction, selectedXData, selectedYData, selectedDetailsData, selectedCorrelationAttrData, selectedCorrelationObjData, selectedLagAttrData, selectedLagObjData)



    console.log(isTextAnnotationEnableList, isDetailsEnableList, selectedDetailsAttrList,isAnnotationsEnabled)



    var detail_attrs = []

    var detail_data = null

    if ("detail_annotation" in annotations) {
        detail_data = JSON.parse(annotations["detail_annotation"]["data_details"]);
        // detail_data = JSON.parse(annotations["detail_annotation"]["data_details"])
        Object.keys(detail_data[0]).forEach(key => {
            if (key != x_name && key != y_scale_keyword) {
                detail_attrs.push(key)
            }
        });
    }

    var menu_items = reactive([])
    updateMenuItems()
    function updateMenuItems() {
        menu_items = []
        Object.keys(annotations).forEach(key => {
            if (key == "text_description_annotation") {
                menu_items.push({
                    clickClose: false,
                    label: h('label', {
                        for: "svg_index_" + index + "_" + "description" + start + end,
                        style: {
                            display: 'inline-block',
                            alignItems: 'center',
                            cursor: 'pointer',
                        },
                    }, [
                        h('span', {
                            style: {
                                fontSize: '13px',
                                color: '#f98',
                                display: 'inline-block',
                                verticalAlign: 'middle',
                            }
                        }, 'description '),
                        h('input', {
                            type: 'checkbox',
                            name: 'description',
                            id: "svg_index_" + index + "_" + "description" + start + end,
                            checked: isTextAnnotationEnableList[i].value,
                            onInput: () => {
                                console.log('Checkbox state changed');
                            },
                            onchange: function () {
                                isTextAnnotationEnableList[i].value = !isTextAnnotationEnableList[i].value
                                if (this.checked) {
                                    const selectedElement = svg.select("#svg_index_" + index + "_" + "textannotation" + start + end);
                                    selectedElement.attr("display", "block").style("z-index", 9999)

                                    // 将选中的元素移动到其父元素的最后，使其在视觉上位于最顶层
                                    selectedElement.node().parentNode.appendChild(selectedElement.node());
                                } else {
                                    const selectedElement = svg.select("#svg_index_" + index + "_" + "textannotation" + start + end);
                                    selectedElement.attr("display", "none");

                                    // 将选中的元素移动到其父元素的最后，使其在视觉上位于最顶层
                                    selectedElement.node().parentNode.appendChild(selectedElement.node());
                                }
                            },
                            style: {
                                verticalAlign: 'middle',
                                marginLeft: '2px'
                            },
                        }),
                    ]),
                    icon: h('img', {
                        src: '/icons/text.png',
                        style: {
                            width: '20px',
                            height: '20px',
                        }
                    }),
                },)
            } else if (key == "detail_annotation") {

                var child = []

                detail_attrs.forEach((attr) => {
                    child.push({
                        clickClose: false,
                        label: h('label', {
                            for: "svg_index_" + index + "_" + "details_" + attr + start + end,
                            style: {
                                display: 'inline-block',
                                alignItems: 'center',
                                cursor: 'pointer',
                            },
                        }, [
                            h('span', {
                                style: {
                                    fontSize: '13px',
                                    color: '#f98',
                                    display: 'inline-block',
                                    verticalAlign: 'middle',
                                }
                            }, attr),
                            h('input', {
                                type: 'radio',
                                name: "svg_index_" + index + "_" + "details_" + start + end,
                                id: "svg_index_" + index + "_" + "details_" + attr + start + end,
                                onInput: () => {
                                    console.log('Checkbox state changed');
                                },
                                checked: attr === selectedDetailsAttrList[i].value,
                                onchange: function () {
                                    this.checked = true;  // 确保选中点击的单选框
                                    selectedDetailsAttrList[i].value = attr
                                },
                                style: {
                                    verticalAlign: 'middle',
                                    marginLeft: '2px'
                                },
                                disabled: !isDetailsEnableList[i].value
                            }),
                        ])
                    })
                })


                menu_items.push({
                    clickClose: false,
                    label: h('label', {
                        for: "svg_index_" + index + "_" + "details" + start + end,
                        style: {
                            display: 'inline-block',
                            alignItems: 'center',
                            cursor: 'pointer',
                        },
                    }, [
                        h('span', {
                            style: {
                                fontSize: '13px',
                                color: '#f98',
                                display: 'inline-block',
                                verticalAlign: 'middle',
                            }
                        }, 'data_details'),
                        h('input', {
                            type: 'checkbox',
                            name: 'details',
                            id: "svg_index_" + index + "_" + "details" + start + end,
                            onInput: () => {
                                console.log('Checkbox state changed');
                            },
                            onchange: function () {
                                console.log('改变了——————————————————————————————————');
                                // 获取当前复选框的状态
                                const isChecked = this.checked;

                                detail_attrs.forEach((attr) => {
                                    const childInput = document.getElementById("svg_index_" + index + "_" + "details_" + attr + start + end);
                                    if (childInput) {
                                        childInput.disabled = !isChecked;
                                    }
                                })

                                isDetailsEnableList[i].value = !isDetailsEnableList[i].value
                            },
                            checked: isDetailsEnableList[i].value,
                            style: {
                                verticalAlign: 'middle',
                                marginLeft: '2px'
                            },
                        }),
                    ]),
                    icon: h('img', {
                        src: '/icons/details.png',
                        style: {
                            width: '20px',
                            height: '20px',
                        }
                    }),
                    children: child
                },)
            } else if (key == "correlation_annotation") {
                menu_items.push({
                    clickClose: false,
                    label: h('label', {
                        for: "svg_index_" + index + "_" + "correlation" + start + end,
                        style: {
                            display: 'inline-block',
                            alignItems: 'center',
                            cursor: 'pointer',
                        },
                    }, [
                        h('span', {
                            style: {
                                fontSize: '13px',
                                color: '#f98',
                                display: 'inline-block',
                                verticalAlign: 'middle',
                            }
                        }, 'correlation'),
                        h('input', {
                            type: 'checkbox',
                            name: 'correlation',
                            id: "svg_index_" + index + "_" + "correlation" + start + end,
                            onInput: () => {
                                console.log('Checkbox state changed');
                            },
                            style: {
                                verticalAlign: 'middle',
                                marginLeft: '2px'
                            },
                        }),
                    ]),
                    icon: h('img', {
                        src: '/icons/corr.png',
                        style: {
                            width: '20px',
                            height: '20px',
                        }
                    }),
                },)
            } else if (key == "lag_annotation") {
                menu_items.push({
                    clickClose: false,
                    label: h('label', {
                        for: "svg_index_" + index + "_" + "lag" + start + end,
                        style: {
                            display: 'inline-block',
                            alignItems: 'center',
                            cursor: 'pointer',
                        },
                    }, [
                        h('span', {
                            style: {
                                fontSize: '13px',
                                color: '#f98',
                                display: 'inline-block',
                                verticalAlign: 'middle',
                            }
                        }, 'time_delag'),
                        h('input', {
                            type: 'checkbox',
                            name: 'time_lag',
                            id: "svg_index_" + index + "_" + "lag" + start + end,
                            // checked: (function () {
                            //     var element = d3.select("#textannotation" + start + end);
                            //     if (!element.empty()) {
                            //         const display = svg.select("#textannotation" + start + end).attr("display");
                            //         return display !== "none";
                            //     } else {
                            //         return true
                            //     }
                            // })(),
                            onInput: () => {
                                console.log('Checkbox state changed');
                                // const checkbox = d3.select("#description" + start + end);
                                // const isChecked = checkbox.property("checked");
                                // // checkbox.property("checked", !isChecked);
                                // if (isChecked) {
                                //     svg.select("#textannotation" + start + end).attr("display", "block")
                                // } else {
                                //     svg.select("#textannotation" + start + end).attr("display", "none")
                                // }
                                // console.log(isChecked);
                            },
                            style: {
                                verticalAlign: 'middle',
                                marginLeft: '2px'
                            },
                        }),
                    ]),
                    icon: h('img', {
                        src: '/icons/lag.png',
                        style: {
                            width: '20px',
                            height: '20px',
                        }
                    }),
                },)
            }
        });
    }

    function showMenu(event) {
        event.preventDefault();
        // 在此处显示自定义的右键菜单
        ContextMenu.showContextMenu({
            x: event.x,
            y: event.y,
            theme: "mac",
            items: menu_items,
            onClose: updateMenuItems
        });
        console.log('右键菜单被触发')
    }
    function highlight_line(svg, data, line, xScale, yScale, x_scale_keyword, y_scale_keyword, start, end, index, pattern, timeduration) {

        const g = svg.append("g").attr("id", "svg_index_" + index + "_" + pattern + "_" + start + "_" + end + "_vis")

        g
            .append("path")
            .datum(data.slice(start, end + 1)) // 
            .attr("fill", "none")
            .attr("stroke", "green") // 高亮颜色
            .attr("stroke-width", 4) // 高亮线段的宽度
            .attr("stroke-opacity", 0.7) // 设置透明度
            .attr("filter", "url(#glow)") // 添加过滤器引用
            .attr("d", line)
            .attr("cursor", "pointer")
            .on('contextmenu', showMenu)
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);



        g.append("g").selectAll('circle')
            .data([data[start], data[end]])  // Start and end points
            .enter().append('circle')
            .attr('cx', d => xScale(d[x_scale_keyword]))
            .attr('cy', d => yScale(d[y_scale_keyword]))
            .attr('r', 4)
            .attr("filter", "url(#glow)")
            .attr('fill', 'red')
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);


        // 添加一个定义过滤器的<defs>元素
        const defs = svg.append("defs");

        // 在<defs>中添加一个<filter>元素，并设置其ID
        const filter = defs.append("filter")
            .attr("id", "glow")
            .attr("x", "-200%")
            .attr("y", "-200%")
            .attr("width", "400%")
            .attr("height", "400%");

        // 在<filter>中添加一个<feGaussianBlur>元素来创建模糊效果
        filter.append("feGaussianBlur")
            .attr("stdDeviation", "2.5") // 模糊程度
            .attr("result", "coloredBlur");

        // 添加一个<feMerge>元素来合并效果
        const feMerge = filter.append("feMerge");

        // 将模糊效果和原始图形合并
        feMerge.append("feMergeNode")
            .attr("in", "coloredBlur");

        feMerge.append("feMergeNode")
            .attr("in", "SourceGraphic");
    }

    if (pattern == "prediction") {
        if (isAnnotationsEnabled[isAnnotationsEnabled.length - 1]) {
            const hasTrue = isAnnotationsEnabled.slice(0, isAnnotationsEnabled.length - 1).some(element => element === true);
            //预测
            if (hasTrue) {
                add_prediction_annotation(svg, data, line, xScale, yScale, x_scale_keyword, y_scale_keyword, prediction_start_index, index, start, end, 1500)
            } else {
                add_prediction_annotation(svg, data, line, xScale, yScale, x_scale_keyword, y_scale_keyword, prediction_start_index, index, start, end, 750)
            }
        }
    } else {
        if (isAnnotationsEnabled[i]) {
            if (isDetailsEnableList[i].value == true) {
                add_details_annotation(svg, detail_data,data_X_Y_without_prediction, xScale, yScale, x_scale_keyword, y_scale_keyword, index, start, end, aggregation, selectedDetailsAttrList[i], x_name, y_name, 1000)
            }
            highlight_line(svg, data, line, xScale, yScale, x_scale_keyword, y_scale_keyword, start, end, index, pattern, 500)
            //文本注释
            let textAnchorPoint = data[Math.floor((start + end) / 2)];
            let textAnchorX = xScale(Math.floor((start + end) / 2));
            let textAnchorY = yScale(textAnchorPoint[y_scale_keyword]);
            let text_annotation = annotations["text_description_annotation"]["description"]
            add_text_annotations(svg, textAnchorX, textAnchorY, text_annotation, start, end, index, 1000)
        }
    }
    // watch(() => [...isAnnotationsEnabled], (newItems, oldItems) => {
    //     console.log("+++++++++++++++++++++++++++++++++++++")
    //     console.log(newItems, oldItems)
    //     newItems.forEach((item, indx) => {
    //         //先擦除
    //         let contentToToggle = d3.select("#svg_index_" + index + "_" + pattern + "_" + start + "_" + end + "_vis");
    //         if (contentToToggle) { contentToToggle.remove() }
    //         let contentToToggleText = d3.select("#svg_index_" + index + "_" + "textannotation" + start + end);
    //         if (contentToToggleText) { contentToToggleText.remove() }
    //         let contentToToggleDetails = d3.select("#svg_index_" + index + "_details_" + start + "_" + end + "_vis");
    //         if (contentToToggleDetails) { contentToToggleDetails.remove() }

    //         if (item !== oldItems[indx] && indx == i) {
    //             if (indx != annotationsList.length - 1) {
    //                 //根据动作状态改变数据空间
    //                 if (item) {
    //                     console.log("")
    //                 }
    //             } else {
    //                 if (item) {
    //                     selectedXData.splice(0, selectedXData.length, ...data_X_Y_with_prediction);
    //                     selectedYData.splice(0, selectedYData.length, ...data_X_Y_with_prediction);
    //                 } else {
    //                     selectedXData.splice(0, selectedXData.length, ...data_X_Y_without_prediction);
    //                     selectedYData.splice(0, selectedYData.length, ...data_X_Y_without_prediction);
    //                 }
    //             }
    //         }
    //     });
    // })
}