import React, { Component } from 'react';
import DatePicker, { registerLocale } from "react-datepicker";
import UIkit from 'uikit';

import { TextEditor } from '../text-editor';
import SelectSearch, { fuzzySearch } from 'react-select-search';

import "react-datepicker/dist/react-datepicker.css";

import ru from 'date-fns/locale/ru';
registerLocale('ru', ru)


export default class TasksModal extends Component {
    constructor(props) {
        super(props);

        this.state = {
            currentTask: props.task,
            isNew: props.isNew,
            subjects: props.subjects,
            timetable: []
        }

        this.isNew = props.isNew;

        this.onClose = props.onClose;
        this.onEdit = props.onEdit;
        this.onSave = props.onSave;
        this.onDelete = props.onDelete;

        this.loadTimetableByDate = props.loadTimetableByDate;
    }

    componentDidMount() {
        const { currentTask, isNew } = this.state;

        UIkit.util.on(`#homework-modal-${isNew ? 'new' : currentTask.id}`, 'hidden', () => {
            const modal = document.getElementById(`homework-modal-${isNew ? 'new' : currentTask.id}`)
            if (modal !== null) {
                modal.remove();
            }

            this.onClose();
        });
        UIkit.modal(`#homework-modal-${isNew ? 'new' : currentTask.id}`).toggle();

        this.loadTimetable(currentTask.date);
    }

    loadTimetable(date) {
        this.loadTimetableByDate(date)
            .then(timetable => {
                this.setState(() => { return { timetable } });
            })
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при загрузке', 'danger')
            })
    }

    handleSubjectChange = (value) => {
        this.setState((state) => {
            const currentTask = state.currentTask;
            currentTask.subject.codename = value;
            return { currentTask }
        });
    }

    handleInfoChange = (value) => {
        this.setState((state) => {
            const currentTask = state.currentTask;
            currentTask.text = value;
            return { currentTask }
        });
    }

    handleDateChange = (value) => {
        this.setState((state) => {
            const currentTask = state.currentTask;
            currentTask.date = value.toISOString().split('T')[0];

            this.loadTimetable(currentTask.date);
            return { currentTask }
        });
    }

    handleEditSubmit = (e) => {
        e.preventDefault();

        const { currentTask } = this.state;

        this.onEdit(currentTask, this.closeModal);
    }

    handleCreateSubmit = (e) => {
        e.preventDefault();

        const { currentTask } = this.state;

        this.onSave(currentTask, this.closeModal);
    }

    handleDelete = (e) => {
        e.preventDefault();

        const { currentTask } = this.state;

        this.onDelete(currentTask, this.closeModal);
    }


    closeModal = () => {
        const { isNew, currentTask } = this.state;

        UIkit.modal(`#homework-modal-${isNew ? 'new' : currentTask.id}`).hide();
    }

    render() {
        const { currentTask, isNew, subjects, timetable } = this.state;

        let options = [];

        if (timetable) {
            const subjectsCodenames = timetable.map(subject => subject.codename)
            const allSubjects = subjects.filter(subject => !subjectsCodenames.includes(subject.codename))

            options = [...timetable.map(subject => {
                return {
                    name: subject.name,
                    value: subject.codename
                }
            }),
            {
                type: 'group',
                name: 'Не по расписанию',
                items: allSubjects.map(subject => {
                    return {
                        name: subject.name,
                        value: subject.codename
                    }
                })
            }]
        } else {
            options = subjects.map(subject => {
                return {
                    name: subject.name,
                    value: subject.codename
                }
            })
        }

        return (
            <div>
                <div id={`homework-modal-${isNew ? 'new' : currentTask.id}`} className="uk-flex-top" uk-modal="true" >
                    <div className="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">

                        <h2 className="uk-modal-title">{this.isNew ? <span>Новое задание</span> : currentTask.subject.name}</h2>

                        <div className="uk-form-stacked" >
                            <div className="uk-margin">
                                <label className="uk-form-label" htmlFor="audience">Предмет</label>
                                <div className="uk-form-controls">
                                    <SelectSearch
                                        className="select-search uk-input"
                                        value={currentTask.subject.codename}
                                        options={options}
                                        search
                                        filterOptions={fuzzySearch}
                                        emptyMessage="Не найдено"
                                        placeholder="Выберите предмет"
                                        onChange={this.handleSubjectChange}
                                    />
                                </div>
                            </div>

                            <div className="uk-margin">
                                <label className="uk-form-label" htmlFor="audience">Дата</label>
                                <div className="uk-form-controls">
                                    <DatePicker className="uk-input" placeholder="Дата" onChange={this.handleDateChange} selected={new Date(currentTask.date)} dateFormat="dd/MM/yyyy" locale="ru" />
                                </div>
                            </div>

                            <div className="uk-margin">
                                <label className="uk-form-label">Информация</label>
                                <div className="uk-form-controls">
                                    <TextEditor onChange={this.handleInfoChange} value={currentTask.text} />
                                </div>
                            </div>

                            <p className="uk-text-right">


                                {this.isNew ?
                                    <button className="uk-button uk-button-primary" onClick={this.handleCreateSubmit}>Создать</button> :
                                    <>
                                        <button className="uk-button uk-button-primary" onClick={this.handleEditSubmit}>Сохранить</button>
                                        <button className="uk-button uk-button-danger" onClick={this.handleDelete} style={{ marginLeft: 10 }}>Удалить</button>
                                    </>
                                }
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}