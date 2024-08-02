// import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
// import ContextMenu from '@imengyu/vue3-context-menu'
// // import hide from '@/assets/icons/hide.svg';
// import { h, reactive } from "vue"
import * as d3 from "d3";
export function add_prediction_annotation(svg, data, line, xScale, yScale, x_name, y_name, prediction_start_index, index, start, end, timeduration) {
    const el = d3.select("#svg_index_" + index + "_prediction_" + start + "_" + end + "_vis")

    if (el.empty())  {

        const g = svg.append("g").attr("id", "svg_index_" + index + "_prediction_" + start + "_" + end + "_vis")

        g.append("path")
            .datum(data.slice(prediction_start_index - 1, data.length))
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 3)
            .attr("stroke-dasharray", "10,5")
            .attr("d", line)
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);


        // 定义up线生成器
        const line_up = d3
            .line()
            .x((d) => xScale(d["index"]))
            .y((d) => yScale(d["up"]));

        g.append("path")
            .datum(data.slice(prediction_start_index - 1, data.length))
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("stroke-dasharray", "5,5")
            .attr("d", line_up)
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);


        // 定义low线生成器
        const line_low = d3
            .line()
            .x((d) => xScale(d["index"]))
            .y((d) => yScale(d["low"]));

        g.append("path")
            .datum(data.slice(prediction_start_index - 1, data.length))
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 2)
            .attr("stroke-dasharray", "5,5")
            .attr("d", line_low)
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);


        // 定义区域生成器
        const area = d3
            .area()
            .x((d) => xScale(d["index"]))
            .y0((d) => yScale(d["low"]))
            .y1((d) => yScale(d["up"]));

        // 绘制填充区域
        g.append("path")
            .datum(data.slice(prediction_start_index - 1, data.length))
            .attr("fill", "rgba(128, 0, 128, 0.1)")
            .attr("d", area)
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);


        g.append("g").selectAll('polygon')
            .data([data[prediction_start_index - 1]]) // Start and end points
            .enter().append('polygon')
            .attr('points', d => `${xScale(d[x_name])},${yScale(d[y_name]) - 5} ${xScale(d[x_name]) - 5},${yScale(d[y_name]) + 5} ${xScale(d[x_name]) + 5},${yScale(d[y_name]) + 5}`)
            .attr('fill', "rgba(128, 0, 128, 0.7)")
            .attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);
    }


    // g.append("g").selectAll('circle')
    //     .data([data[prediction_start_index - 1]])  // Start and end points
    //     .enter().append('circle')
    //     .attr('cx', d => xScale(d[x_name]))
    //     .attr('cy', d => yScale(d[y_name]))
    //     .attr('r', 4)
    //     // .attr("filter", "url(#glow)")
    //     .attr('fill', "rgba(128, 0, 128, 1)")
}
