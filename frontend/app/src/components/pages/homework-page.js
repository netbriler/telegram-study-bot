import FullCalendar from '@fullcalendar/react';

import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import UIkit from 'uikit';

import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';
import { PageTemplate } from '../page-templates';
import TasksModal from '../tasks-modal';

class HomeworkPage extends Component {
    title = 'Домашнее задания'
    description = 'Календарь с домашними заданиями'
    icon = 'ion-android-people'

    calendarComponentRef = React.createRef()

    constructor(props) {
        super(props);

        this.state = {
            tasks: [],
            selectedTask: null,
            weekendsVisible: false
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;

        this.currentTaskId = props.match.params.id;
    }

    componentDidMount() {
        if (this.currentTaskId != null) {
            this.isLoading();
            this.loadTask(this.currentTaskId, this.isLoaded);
        }
    }

    loadTask(id, callback) {
        this.AdminService.getTask(id)
            .then(task => {
                if (task == null) {
                    return this.props.history.push('/homework')
                }

                this.goToDate(new Date(task.date));
                this.setState(() => { return { selectedTask: task } });
                this.props.history.push('/homework/' + task.id);
            })
            .finally(callback);
    }

    showNotification = (message, status) => {
        UIkit.notification({ message, status });
    }

    handleDates = (rangeInfo) => {
        this.isLoading();

        const fromDate = rangeInfo.startStr.split('T')[0];
        const endDate = rangeInfo.endStr.split('T')[0];

        this.AdminService.getTasksCalendar(fromDate, endDate)
            .then(tasks => {
                this.setState({ tasks });
            })
            .finally(this.isLoaded);
    }

    handleDateSelect = (selectInfo) => {
        console.log('selected: ', selectInfo)
    }

    handleEventChange = (changeInfo) => {
        console.log(changeInfo);
    }

    handleEventClick = (info) => {
        this.isLoading();
        this.loadTask(info.event.id, this.isLoaded);
    }

    handleTaskChange = (task) => {
        console.log(task);
    }

    handleTaskEditClose = () => {
        this.setState({ selectedTask: null });
        this.props.history.push('/homework');
    }

    toggleWeekends = () => {
        const { weekendsVisible } = this.state;

        this.setState({ weekendsVisible: !weekendsVisible });
    }

    goToDate = (date) => {
        const calendarApi = this.calendarComponentRef.current.getApi();

        if (calendarApi.view.activeStart.getTime() < date.getTime() && date.getTime() < calendarApi.view.activeEnd.getTime()) {
            return
        }

        calendarApi.gotoDate(date);
    };

    render() {
        const { tasks, selectedTask, weekendsVisible } = this.state;

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
                        weekends={weekendsVisible}
                        events={tasks}
                        eventDrop={this.drop}
                        eventReceive={this.eventReceive}
                        eventChange={this.handleEventChange}
                        datesSet={this.handleDates}
                        select={this.handleDateSelect}
                        eventClick={this.handleEventClick}

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
                {selectedTask != null ? <TasksModal task={selectedTask} onClose={this.handleTaskEditClose} /> : ''}
            </PageTemplate>
        )
    }
}


const mapStateToProps = (state) => {
    return {}
}

const mapDispatchToProps = {
    isLoaded,
    isLoading
}


export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(HomeworkPage));