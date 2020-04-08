import React from 'react';
import * as d3 from 'd3';


class LabAnalysis extends React.Component {
    drawBarChart(topics) {
        const data = Object.entries(topics)
        .map(item => { return {topic: item[0], score: item[1]}})
        .sort((a, b) => b.score - a.score);

        const total_width = 800;
        const total_height = 200;
        const legend_width = 400;
        const margin = {top: 20, right: 0, bottom: 10, left: 30};
        const chart_width = total_width - legend_width - margin.left - margin.right;
        const chart_height = total_height - margin.top - margin.bottom;

        let svg = d3.select(".topics-viz")
            .append("svg")
            .attr("width", total_width)
            .attr("height", total_height)
            .append("g")
            .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

        const x = d3.scaleBand()
            .range([0, chart_width])
            .padding(0.2)
            .domain(data.map(sample => sample.topic));

        svg.append("g")
            .attr("transform", "translate(0," + chart_height + ")");

        const y = d3.scaleLinear()
            .domain([0, 1.0])
            .range([chart_height, 0]);

        svg.append("g")
            .call(d3.axisLeft(y)
                .ticks(4));

        const colorScale = d3.interpolateBlues;

        svg.selectAll("legend-dots")
          .data(data)
          .enter()
          .append("circle")
            .attr("cx", total_width - legend_width)
            .attr("cy", (d,i) => total_height / 10 + i*25)
            .attr("r", 5)
            .style("fill", d => colorScale(1 - x(d.topic)/ chart_width));

        svg.selectAll("legend-dots")
          .data(data)
          .enter()
          .append("text")
            .text(d => d.topic)
            .attr("x", total_width - legend_width + 10)
            .attr("y", (d, i) => total_height / 10 + i*25)
            .attr("font-size", "8px")
            .attr("text-anchor", "left")
            .style("alignment-baseline", "middle");


        svg.selectAll("bar")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", d => x(d.topic))
            .attr("y", d => y(d.score))
            .attr("width", x.bandwidth())
            .attr("height", (d) => chart_height - y(d.score))
            .attr("fill", d => colorScale(1 - x(d.topic)/ chart_width));
    };

    render() {
        this.drawBarChart(this.props.document.topics);
        return <div className="topics-viz"></div>
    }
}

export default LabAnalysis;
