import React, { Component } from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';

import { PageTemplate } from '../page-templates'
import { Timetable } from '../timetable';

import UIkit from 'uikit';


const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

const move = (source, destination, droppableSource, droppableDestination) => {
    const sourceClone = Array.from(source);
    const destClone = Array.from(destination);
    const [removed] = sourceClone.splice(droppableSource.index, 1);


    destClone.splice(droppableDestination.index, 0, removed);

    const result = {};
    result[droppableSource.droppableId - 1] = sourceClone;
    result[droppableDestination.droppableId - 1] = destClone;

    return result;
};


class TimetablePage extends Component {
    title = 'Расписание'
    description = 'Страница редактирования расписания'
    icon = 'ion-edit'

    constructor(props) {
        super(props);

        this.state = {
            timetable: null,
            subjects: []
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.loadTimetable(this.isLoaded);
        this.loadSubjects(this.isLoaded);
    }

    loadSubjects(callback) {
        this.AdminService.getAllSubjects()
            .then(subjects => {
                this.setState(() => { return { subjects } });
            })
            .then(callback);
    }

    loadTimetable(callback) {
        this.AdminService.getTimetable()
            .then(timetable => {
                this.setState(() => {
                    timetable = timetable.map(day => {
                        day.subjects = Object.entries(day.subjects).map(([subjectIndex, subject]) => ({
                            id: `${day.day_id}-${subjectIndex}-${subject.codename}`,
                            content: subject.name,
                            codename: subject.codename
                        }))
                        return day
                    });

                    return { timetable }
                });
            })
            .then(callback);
    }

    onDragEnd = (result) => {
        const { source, destination } = result;
        const { timetable } = this.state;

        // dropped outside the list
        if (!result.destination) {
            return;
        }

        const sInd = +source.droppableId - 1;
        const dInd = +destination.droppableId - 1;

        let newState = [...timetable];

        if (sInd === dInd) {
            const subjects = reorder(
                timetable[dInd].subjects,
                result.source.index,
                result.destination.index
            );
            newState[sInd].subjects = subjects;
        } else {
            const result = move(timetable[sInd].subjects, timetable[dInd].subjects, source, destination);
            newState[sInd].subjects = result[sInd];
            newState[dInd].subjects = result[dInd];
        }

        this.setState({
            timetable: newState
        });
    }

    deleteSubject = (day_id, subject_index) => {
        this.setState(({ timetable }) => {
            delete timetable[day_id - 1]['subjects'][subject_index];

            timetable[day_id - 1]['subjects'] = timetable[day_id - 1]['subjects'].filter(e => e);

            return timetable;
        });
    }

    addSubject = (day, subject) => {
        this.setState(({ timetable }) => {
            timetable[day.day_id - 1]['subjects'].push({
                id: `${day.day_id}-${timetable[day.day_id - 1]['subjects'].length}-${subject.codename}`,
                content: subject.name,
                codename: subject.codename
            });

            return { timetable }
        });
    }

    onTimetableSave = (timetable) => {
        const formatedTimetable = timetable.map((day) => {
            return {
                id: day.day_id,
                subjects: day.subjects.map(subject => subject.codename).join(',')
            }
        })

        this.isLoading();

        this.AdminService.editTimetable(formatedTimetable)
            .then(() => {
                this.showNotification('Сохранено', 'success')
            })
            .then(this.isLoaded)
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при изменении', 'danger')
            });
    }

    showNotification = (message, status) => {
        UIkit.notification({ message, status });
    }

    render() {
        const { timetable, subjects } = this.state;

        if (!timetable) {
            return '';
        }

        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container uk-container-large">
                    <Timetable onDragEnd={this.onDragEnd} timetable={timetable} deleteSubject={this.deleteSubject} addSubject={this.addSubject} subjects={subjects} onTimetableSave={this.onTimetableSave} />
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(TimetablePage));