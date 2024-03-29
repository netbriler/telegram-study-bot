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
    description = 'Здесь можно добавлять, перетаскивать и редактировать домашнее задания'
    icon = 'ion-android-calendar'

    calendarComponentRef = React.createRef()

    constructor(props) {
        super(props);

        this.state = {
            tasks: [],
            subjects: [],
            selectedTask: null,
            isNewTask: false,
            weekendsVisible: false
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;

        this.currentTaskId = props.match.params.id;
    }

    componentDidMount() {
        this.loadSubjects(this.isLoaded);

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
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при загрузке', 'danger')
            })
            .finally(callback);
    }

    loadSubjects(callback) {
        this.AdminService.getAllSubjects()
            .then(subjects => {
                this.setState(() => { return { subjects } });
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
        const newTask = {
            text: '',
            date: selectInfo.startStr,
            subject: { codename: null },
            files: []
        }

        this.setState(() => { return { selectedTask: newTask, isNewTask: true } });
    }

    loadTimetableByDate = (date) => {
        return this.AdminService.getTimetableByDate(date, true)
    }

    handleEventChange = (changeInfo) => {
        const params = {
            date: changeInfo.event.startStr
        };

        this.AdminService.editTask(changeInfo.event.id, params)
            .catch(({ response }) => {
                this.refetchCalendar()
                this.showNotification('Произошла ошибка при изменении', 'danger')
            })
    }

    handleEventClick = (info) => {
        this.isLoading();
        this.loadTask(info.event.id, this.isLoaded);
    }

    handleTaskEditClose = () => {
        this.setState({ selectedTask: null, isNewTask: false });
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
    }

    refetchCalendar = () => {
        const calendarApi = this.calendarComponentRef.current.getApi();

        calendarApi.gotoDate(calendarApi.getDate());
    }

    handleCreateTask = (task, closeModal) => {
        this.isLoading();

        const params = {
            subject_codename: task.subject.codename,
            text: task.text,
            date: task.date,
            files: task.files.filter((file) => (file.title !== '' || file.file_id !== ''))
        };

        this.AdminService.createTask(params)
            .then(() => {
                this.refetchCalendar();
                this.showNotification('Создано', 'success')
            })
            .then(closeModal)
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при создании', 'danger')
            })
            .finally(this.isLoaded);
    }

    handleTaskEdit = (task, closeModal) => {
        this.isLoading();

        const params = {
            subject_codename: task.subject.codename,
            text: task.text,
            date: task.date,
            files: task.files.filter((file) => (file.title !== '' || file.file_id !== ''))
        };

        this.AdminService.editTask(task.id, params)
            .then(() => {
                this.refetchCalendar();
                this.showNotification('Сохранено', 'success')
            })
            .then(closeModal)
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при изменении', 'danger')
            })
            .finally(this.isLoaded);
    }

    handleTaskDelete = (task, closeModal) => {
        UIkit.modal.confirm('Вы точно хотите удалить задание?', { labels: { ok: 'Да', cancel: 'Отмена' }, stack: true })
            .then(() => {
                this.isLoading();
                this.AdminService.deleteTask(task.id)
                    .then(() => {
                        this.refetchCalendar()
                    })
                    .then(closeModal)
                    .catch(({ response }) => {
                        this.showNotification('Произошла ошибка при удалении', 'danger')
                    })
                    .finally(this.isLoaded);
            }, () => { });
    }

    render() {
        const { tasks, selectedTask, isNewTask, subjects, weekendsVisible } = this.state;

        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container">
                    <div className="uk-card uk-card-default uk-card-body">

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
                </div>
                {selectedTask != null ? <TasksModal task={selectedTask} AdminService={this.AdminService} showNotification={this.showNotification} onClose={this.handleTaskEditClose} onEdit={this.handleTaskEdit} onSave={this.handleCreateTask} onDelete={this.handleTaskDelete} loadTimetableByDate={this.loadTimetableByDate} isNew={isNewTask} subjects={subjects} /> : ''}
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