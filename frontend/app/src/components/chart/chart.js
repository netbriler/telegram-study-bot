import React, { Component } from 'react';
import Chart from 'chart.js'

export default class Charts extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: props.data,
            type: props.type,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false,
                },
                tooltips: {
                    bodyFontColor: '#fff',
                },
                scales: {
                    yAxes: [{
                        gridLines: {
                            display: false,
                        },
                    }],
                    xAxes: [{
                        gridLines: {
                            display: false,
                        }
                    }]
                },
                ...props.options
            },
            id: 'chart_' + Math.random().toString(36).substr(2, 9)
        }
    }

    componentDidMount() {
        const { id, data, options, type } = this.state;

        this.current_chart = new Chart(document.getElementById(id), { type, data, options });
    }

    render() {
        return <canvas id={this.state.id} />
    }

}