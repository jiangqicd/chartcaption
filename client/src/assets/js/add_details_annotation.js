import * as d3 from "d3";
export function add_details_annotation(svg, data, rawdata,xScale, yScale, x_scale_keyword, y_scale_keyword, index, start, end, aggregation, selectedDetailsAttr, x_name, y_name, timeduration) {
    console.log("//////////////////////////////////////////////")
    console.log(data)
    console.log(aggregation)

    data.forEach(item_i => {
        rawdata.forEach(item_j => {
            if (item_i[x_name] == item_j[x_name]) {
                item_i["index"] = item_j["index"]
            }
        })
    })
    let rollupData = null
    if (aggregation == "null" || aggregation == "mean") {
        rollupData = d3.rollup(data,
            v => d3.mean(v, d => d[y_name]), // 计算每个组内的 GDP 平均值
            d => d[x_name], // 第一层分组按年份
            d => d[selectedDetailsAttr.value] // 第二层分组按国家
        )
    } else if (aggregation == "max") {
        rollupData = d3.rollup(data,
            v => d3.max(v, d => d[y_name]), // 计算每个组内的 GDP 平均值
            d => d[x_name], // 第一层分组按年份
            d => d[selectedDetailsAttr.value] // 第二层分组按国家
        )
    } else if (aggregation == "min") {
        rollupData = d3.rollup(data,
            v => d3.min(v, d => d[y_name]), // 计算每个组内的 GDP 平均值
            d => d[x_name], // 第一层分组按年份
            d => d[selectedDetailsAttr.value] // 第二层分组按国家
        )
    } else if (aggregation == "sum") {
        rollupData = d3.rollup(data,
            v => d3.sum(v, d => d[y_name]), // 计算每个组内的 GDP 平均值
            d => d[x_name], // 第一层分组按年份
            d => d[selectedDetailsAttr.value] // 第二层分组按国家
        )
    }

    let detail_data = Array.from(rollupData, ([key1, value]) =>
        Array.from(value, ([key2, meanValue]) => ({
            [x_name]: key1,
            [selectedDetailsAttr.value]: key2,
            [y_name]: meanValue
        }))
    ).flat();

    detail_data.forEach(item_i => {
        data.forEach(item_j => {
            if (item_i[x_name] == item_j[x_name]) {
                item_i["index"] = item_j["index"]
            }
        })
    })

    const el = d3.select("#svg_index_" + index + "_details_" + start + "_" + end + "_vis")

    if (el.empty()) {

        const g = svg.append("g").attr("id", "svg_index_" + index + "_details_" + start + "_" + end + "_vis")

        // 添加散点
        g.selectAll("circle")
            .data(detail_data)
            .enter().append("circle")
            .attr("cx", d => xScale(d[x_scale_keyword]))
            .attr("cy", d => yScale(d[y_scale_keyword]))
            .attr("r", 4)
            .style("fill", "#9ecae1") // 使用颜色比例尺设置填充颜色
            .style("stroke", "#9ecae1") // 使用颜色比例尺设置边框颜色
            .style("opacity", 0.7) // 设置透明度为 50%
            .attr("stroke-width", 1)
            .on("mouseover", function (event, d) {
                d3.select(this)
                    .attr("r", 8)
                    .style("opacity", 1);

                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);

                tooltip.html(`${x_name}: ${d[x_name]}<br>${selectedDetailsAttr.value}: ${d[selectedDetailsAttr.value]}<br>${y_name}: ${d[y_name].toFixed(2)}`)
                    .style("left", (event.pageX) + "px")
                    .style("top", (event.pageY) + "px");
            })
            .on("mouseout", function () {
                d3.select(this).transition()
                    .duration(1000)
                    .attr("r", 4)
                    .style("opacity", 0.7) // 设置透明度为 50%

                tooltip.transition()
                    .duration(1000)
                    .style("opacity", 0);
            });
        // .style("fill", "#69b3a2")
        // .style("opacity", 0.1); // 设置透明度为 50%

        // 添加过渡效果
        g.attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);

        // 创建工具提示元素
        const tooltip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
    }

}