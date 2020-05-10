import React from 'react';
import * as d3 from 'd3';
import Typography from '@material-ui/core/Typography';


class LabAnalysis extends React.Component {
    constructor(props) {
        super(props);
        this.state = {selectedTopic: 0};
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(d, i) {
        this.setState({selectedTopic: i})
    }

    drawBarChart(topics) {
        // Clear graph
        d3.selectAll("svg").remove();

        const data = Object.entries(topics)
        .map(item => { return {topic: item[0], score: item[1]}})
        .sort((a, b) => b.score - a.score);

        const total_width = 800;
        const total_height = 300;
        const legend_width = 500;
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

        svg.selectAll("legend")
          .data(data)
          .enter()
          .append("text")
            .text((d, i) => i === this.state.selectedTopic? `Topic keywords: ${d.topic}` : "")
            .attr("x", total_width - legend_width + 10)
            .attr("y", () => total_height / 3)
            .attr("font-size", "14px")
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
            .attr("fill", (d, i) => i === this.state.selectedTopic? "black" : "grey")
            .on("click", this.handleClick);
    };

    render() {
        this.drawBarChart(this.props.document.topics);
        return (
            <div>
                <br/>
                <Typography variant="h4">Document Topics</Typography>
                <Typography variant="body1" gutterBottom><i>Click topics to inspect</i></Typography>
                <br/>
                <div className="topics-viz"></div>
                <br/><br/><br/>
                <Typography variant="h4">Important keywords</Typography>
            </div>

        )
    }
}

export default LabAnalysis;
