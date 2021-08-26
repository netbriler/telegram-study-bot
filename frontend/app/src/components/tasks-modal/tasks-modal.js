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

    render() {
        const { currentTask } = this.state;

        return (
            <div>
                <div id={`homework-modal-${currentTask.id}`} uk-modal="true" >
                    <div className="uk-modal-dialog uk-modal-body">
                        <h2 className="uk-modal-title">{currentTask.subject.name}</h2>

                        <div className="uk-form-stacked" >
                            <div className="uk-margin">
                                <label className="uk-form-label" htmlFor="audience">Дата</label>
                                <div className="uk-form-controls">
                                    <DatePicker className="uk-input" placeholder="Дата" selected={new Date(currentTask.date)} dateFormat="dd/MM/yyyy" locale="ru" />
                                </div>
                            </div>

                            <div className="uk-margin">
                                <label className="uk-form-label">Информация</label>
                                <div className="uk-form-controls">
                                    <TextEditor onChange={() => { }} value={currentTask.text} />
                                </div>
                            </div>

                            <p className="uk-text-right">
                                <button className="uk-button uk-button-primary uk-modal-close" type="button">Ок</button>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}