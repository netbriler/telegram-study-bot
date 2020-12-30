import React, { Component } from 'react';
import Chart from '../chart'
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';

class DashboardPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            data: []
        }

        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.loadData(this.isLoaded);
    }

    loadData(callback) {
        callback();
    }

    render() {
        const data = {
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "Website traffic",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "#F44336",
                    borderColor: "#F44336",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "#F44336",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "#F44336",
                    pointHoverBorderColor: "#F44336",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [103265, 128259, 85290, 115923, 91238, 108295, 102295],
                    spanGaps: false,
                },
                {
                    label: "Website private traffic",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "#32CD32",
                    borderColor: "#32CD32",
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: "#32CD32",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "#32CD32",
                    pointHoverBorderColor: "#32CD32",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [143265, 108259, 65290, 195923, 31238, 168295, 132295],
                    spanGaps: false,
                }
            ]
        };

        return (
            <>
                <div className="content-padder content-background">
                    <div className="uk-section-small uk-section-default header">
                        <div className="uk-container uk-container-large">
                            <h1><span className="ion-speedometer" /> Аналитика</h1>

                            <p>За последние 28 дней было добавлено 34 домашки</p>

                            <ul className="uk-breadcrumb">
                                <li><a href="#">Главная</a></li>
                                <li><span href="#">Аналитика</span></li>
                            </ul>
                        </div>
                    </div>
                    <div className="uk-section-small">
                        <div className="uk-container uk-container-large">
                            <div uk-grid="true" className="uk-child-width-1-1@s uk-child-width-1-2@m uk-child-width-1-4@xl uk-grid">
                                <div className="uk-first-column">
                                    <div className="uk-card uk-card-default uk-card-body">
                                        <span className="statistics-text">Всего сообщений</span><br />
                                        <span className="statistics-number">
                                            1.980
                  <span className="uk-label uk-label-success">
                                                8% <span className="ion-arrow-up-c" />
                                            </span>
                                        </span>
                                    </div>
                                </div>
                                <div>
                                    <div className="uk-card uk-card-default uk-card-body">
                                        <span className="statistics-text">Личных сообщений</span><br />
                                        <span className="statistics-number">
                                            123.238
                  <span className="uk-label uk-label-danger">
                                                13% <span className="ion-arrow-down-c" />
                                            </span>
                                        </span>
                                    </div>
                                </div>
                                <div>
                                    <div className="uk-card uk-card-default uk-card-body">
                                        <span className="statistics-text">Груповых сообщений</span><br />
                                        <span className="statistics-number">
                                            2.316
                  <span className="uk-label uk-label-success">
                                                37% <span className="ion-arrow-up-c" />
                                            </span>
                                        </span>
                                    </div>
                                </div>
                                <div>
                                    <div className="uk-card uk-card-default uk-card-body">
                                        <span className="statistics-text">Всего домашек</span><br />
                                        <span className="statistics-number">
                                            38
                  <span className="uk-label uk-label-success">
                                                26% <span className="ion-arrow-up-c" />
                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div uk-grid="true" className="uk-child-width-1-1@s uk-child-width-1-2@l uk-grid">
                                <div className="uk-first-column">
                                    <div className="uk-card uk-card-default">
                                        <div className="uk-card-header">Трафик в личке</div>

                                        <div className="uk-card-body">
                                            <Chart type={'line'} data={data} />
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <div className="uk-card uk-card-default">
                                        <div className="uk-card-header">Трафик в группе</div>

                                        <div className="uk-card-body">
                                            <Chart type={'bar'} data={data} />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        loading: state.loading
    }
}


const mapDispatchToProps = {
    isLoaded,
    isLoading
}

export default connect(mapStateToProps, mapDispatchToProps)(DashboardPage);