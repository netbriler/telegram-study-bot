import React, { Component } from 'react';
import DatePicker, { registerLocale } from "react-datepicker";
import UIkit from 'uikit';

import { TextEditor } from '../text-editor';

import "react-datepicker/dist/react-datepicker.css";

import ru from 'date-fns/locale/ru';
registerLocale('ru', ru)


export default class TasksModal extends Component {
    constructor(props) {
        super(props);

        this.state = {
            currentTask: props.task
        }

        this.onClose = props.onClose;
        this.onEdit = props.onEdit;
        this.onDelete = props.onDelete;
    }

    componentDidMount() {
        const { currentTask } = this.state;

        UIkit.util.on(`#homework-modal-${currentTask.id}`, 'hidden', () => {
            const modal = document.getElementById(`homework-modal-${currentTask.id}`)
            if (modal !== null) {
                modal.remove();
            }

            this.onClose();
        });
        UIkit.modal(`#homework-modal-${currentTask.id}`).toggle();
    }

    static getDerivedStateFromProps(props, state) {
        return { currentTask: props.task }
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
            return { currentTask }
        });
    }

    handleEditSubmit = (e) => {
        e.preventDefault();

        const { currentTask } = this.state;

        this.onEdit(currentTask, this.closeModal);
    }

    handleDelete = (e) => {
        e.preventDefault();

        const { currentTask } = this.state;

        this.onDelete(currentTask, this.closeModal);
    }


    closeModal = () => {
        const { currentTask } = this.state;

        UIkit.modal(`#homework-modal-${currentTask.id}`).hide();
    }

    render() {
        const { currentTask } = this.state;

        return (
            <div>
                <div id={`homework-modal-${currentTask.id}`} className="uk-flex-top" uk-modal="true" >
                    <div className="uk-modal-dialog uk-modal-body uk-margin-auto-vertical">
                        <h2 className="uk-modal-title">{currentTask.subject.name}</h2>

                        <div className="uk-form-stacked" >
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
                                <button className="uk-button uk-button-primary" onClick={this.handleEditSubmit}>Сохранить</button>
                                <button className="uk-button uk-button-danger" onClick={this.handleDelete} style={{ marginLeft: 10 }}>Удалить</button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}