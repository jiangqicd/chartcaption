/* eslint-disable no-inner-declarations */
import timeSeriesVocabulary from './ts_description_keywords.js';
import * as d3 from "d3";
export function add_text_annotations(svg, targetX, targetY, description, start, end, index, timeduration) {

    const el = d3.select("#svg_index_" + index + "_" + "textannotation" + start + end)

    if (el.empty()) {
        // Add annotation group
        const annotation = svg.append("g")
            .attr("class", "textannotation")
            .attr("id", "svg_index_" + index + "_" + "textannotation" + start + end)
            .attr("cursor", "move")
            .attr("user-select", "none")
            .call(d3.drag().on("drag", dragged))

        function appendWrappedText(annotation, text, x, y, maxWidth, lineHeight) {
            const words = text.split(" ");

            const textElement = annotation.append("text")
                .attr("x", x)
                .attr("y", y)
                .attr("text-anchor", "middle")
                .style("fill", "black")
                .style("font-size", "12px");

            let line = "";
            let lineNumber = 0;

            words.forEach(word => {
                const testLine = line + " " + word;
                const testWidth = testLine.length * 6; // 估算文本宽度，假设每个字符的宽度为6像素

                if (testWidth > maxWidth) {
                    appendTspan(annotation, textElement, line, x, y, lineNumber, lineHeight);
                    line = word;
                    lineNumber++;
                } else {
                    line = testLine;
                }
            });

            appendTspan(annotation, textElement, line, x, y, lineNumber, lineHeight);

            return textElement;
        }

        function appendTspan(annotation, textElement, line, x, y, lineNumber, lineHeight) {
            const tspan = textElement.append("tspan")
                .attr("x", x)
                .attr("y", y)
                .attr("class", "d-tspan")
                .attr("dy", `${lineNumber * lineHeight}px`);

            const words = line.split(" ");

            words.forEach(word => {
                const isNumber = !isNaN(parseFloat(word));
                const isPattern = timeSeriesVocabulary.includes(word);

                if (isNumber) {
                    tspan.append("tspan")
                        .style("fill", "#e41a1c")
                        .style("font-weight", "bold")
                        .attr("class", "n-tspan")
                        // .style('text-decoration', 'underline')
                        .text(word + " ");
                } else if (isPattern) {
                    tspan.append("tspan")
                        .style("fill", "orange")
                        .style("font-weight", "bold")
                        .attr("class", "p-tspan")
                        // .style('text-decoration', 'underline')
                        .text(word + " ");
                } else {
                    tspan.append("tspan")
                        .text(word + " ");
                }
            });

            var ntspans = tspan.selectAll(".n-tspan")
            // 遍历每个tspan元素
            ntspans.each(function () {
                var ts = d3.select(this);

                var bbox = {}

                // 获取tspan的尺寸信息
                if (ts.node()) {
                    bbox = this.getBBox();
                }

                // 创建一个矩形作为边框
                annotation.append('rect') // 插入位置可以根据需要调整
                    .attr('x', bbox.x)
                    .attr('y', bbox.y)
                    .attr('width', bbox.width - 6)
                    .attr('height', bbox.height)
                    .attr('fill', "#e41a1c") // 边框背景透明
                    // .attr('stroke', 'red') // 边框颜色
                    .attr('fill-opacity', 0.2)
                // .attr('stroke-width', '1px'); // 边框宽度
            });

            var ptspans = tspan.selectAll(".p-tspan")
            // 遍历每个tspan元素
            ptspans.each(function () {
                var ts = d3.select(this);

                var bbox = {}

                // 获取tspan的尺寸信息
                if (ts.node()) {
                    bbox = this.getBBox();
                }

                // 创建一个矩形作为边框
                annotation.append('rect') // 插入位置可以根据需要调整
                    .attr('x', bbox.x)
                    .attr('y', bbox.y)
                    .attr('width', bbox.width - 6)
                    .attr('height', bbox.height)
                    .attr('fill', 'orange') // 边框背景透明
                    // .attr('stroke', 'red') // 边框颜色
                    .attr('fill-opacity', 0.2)
                // .attr('stroke-width', '1px'); // 边框宽度
            });
        }

        const text = appendWrappedText(annotation, description, targetX + 20, targetY - 100, 250, 12)

        var bbox = {}
        if (text.node() !== null) {
            // 元素已被渲染
            bbox = text.node().getBBox();
            // 执行其他操作
        }


        const rect = annotation.insert("rect", "text")
            .attr("x", bbox.x - 5)
            .attr("y", bbox.y - 5)
            .attr("width", bbox.width + 10)
            .attr("height", bbox.height + 10)
            .attr("fill", "white")
            .attr("stroke", "gray")
            .attr("rx", 5)
            .attr("ry", 5)


        const line1 = annotation.append("line")
            .attr("x1", bbox.x + bbox.width / 2)
            .attr("y1", bbox.y + bbox.height + 5)
            .attr("x2", targetX)
            .attr("y2", targetY)
            .attr("stroke", "gray")
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)")

        // 添加过渡效果
        annotation.attr("opacity", 0)
            .transition().delay(timeduration).duration(timeduration)
            .attr("opacity", 1);

        function dragged(event) {
            const dx = event.dx;
            const dy = event.dy;

            text.attr("x", parseFloat(text.attr("x")) + dx)
                .attr("y", parseFloat(text.attr("y")) + dy)


            text.selectAll(".d-tspan").attr("x", function () {
                return parseFloat(d3.select(this).attr("x")) + dx;
            })
                .attr("y", function () {
                    return parseFloat(d3.select(this).attr("y")) + dy;
                });

            annotation.selectAll("rect").attr("x", function () {
                return parseFloat(d3.select(this).attr("x")) + dx;
            })
                .attr("y", function () {
                    return parseFloat(d3.select(this).attr("y")) + dy;
                });

            line1.attr("x1", parseFloat(line1.attr("x1")) + dx)
                .attr("y1", parseFloat(line1.attr("y1")) + dy);

            if (parseFloat(line1.attr("y1")) > parseFloat(line1.attr("y2"))) {
                line1.attr("y1", parseFloat(rect.attr("y")))
            }
            if (parseFloat(line1.attr("y1")) < parseFloat(line1.attr("y2"))) {
                line1.attr("y1", parseFloat(rect.attr("y")) + parseFloat(rect.attr("height")))
            }
            if (parseFloat(rect.attr("x")) + parseFloat(rect.attr("width")) < parseFloat(line1.attr("x2"))) {
                line1.attr("x1", parseFloat(rect.attr("x")) + parseFloat(rect.attr("width"))).attr("y1", parseFloat(rect.attr("y")) + parseFloat(rect.attr("height") / 2))
            } else if (parseFloat(rect.attr("x")) > parseFloat(line1.attr("x2"))) {
                line1.attr("x1", parseFloat(rect.attr("x"))).attr("y1", parseFloat(rect.attr("y")) + parseFloat(rect.attr("height") / 2))
            } else {
                line1.attr("x1", parseFloat(rect.attr("x")) + parseFloat(rect.attr("width")) / 2)
            }

        }

        // Define the arrowhead marker
        svg.append("defs").append("marker")
            .attr("id", "arrow")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 5)
            .attr("refY", 0)
            .attr("markerWidth", 4)
            .attr("markerHeight", 4)
            .attr("orient", "auto-start-reverse")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "black");
    }

}