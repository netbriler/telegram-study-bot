import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import UIkit from 'uikit';

import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';
import { PageTemplate } from '../page-templates';

class HomeworkPage extends Component {
    title = 'Домашнее задания'
    description = 'Календарь с домашними заданиями'
    icon = 'ion-android-people'

    calendarComponentRef = React.createRef()
    state = {
        tasks: [],
        weekendsVisible: false
    }

    constructor(props) {
        super(props);

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }


    showNotification = (message, status) => {
        UIkit.notification({ message, status });
    }

    handleDates = (rangeInfo) => {
        const fromDate = rangeInfo.startStr.split('T')[0];
        const endDate = rangeInfo.endStr.split('T')[0];

        this.AdminService.getTasksCalendar(fromDate, endDate)
            .then(tasks => {
                this.setState(() => { return { tasks } });
            })
    }

    handleDateSelect = (selectInfo) => {
        console.log('selected: ', selectInfo)
    }

    handleEventChange = (changeInfo) => {
        console.log(changeInfo);
    }

    toggleWeekends = () => {
        const {weekendsVisible} = this.state; 

        this.setState({ weekendsVisible:!weekendsVisible });
    }

    render() {
        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container uk-section-default">
                    <FullCalendar
                        plugins={[dayGridPlugin, interactionPlugin]}
                        headerToolbar={{
                            left: 'prev,next today',
                            center: 'title',
                            right: 'dayGridMonth,dayGridWeek,dayGridDay'
                        }}
                        defaultView="dayGridMonth"

                        rerenderDelay={10}
                        editable={true}
                        eventDurationEditable={false}
                        selectable={true}
                        selectMirror={true}
                        weekNumbers={true}
                        weekText={'Неделя '}

                        selectAllow={(e) => e.end.getTime() / 1000 - e.start.getTime() / 1000 <= 86400}

                        dayMaxEvents={true}

                        locale="ru"
                        firstDay={1}
                        buttonText={{
                            today: 'сегодня',
                            month: 'месяц',
                            week: 'неделя',
                            day: 'день',
                            list: 'список'
                        }}

                        ref={this.calendarComponentRef}
                        weekends={this.state.weekendsVisible}
                        events={this.state.tasks}
                        eventDrop={this.drop}
                        eventReceive={this.eventReceive}
                        eventChange={this.handleEventChange}
                        datesSet={this.handleDates}
                        select={this.handleDateSelect}

                    />
                    <label>
                        <input
                            type='checkbox'
                            checked={this.state.weekendsVisible}
                            onChange={this.toggleWeekends}
                        ></input>
                        показывать выходные дни
                    </label>
                </div>
            </PageTemplate>
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(HomeworkPage));