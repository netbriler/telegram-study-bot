import React, { Component } from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';

import { PageTemplate } from '../page-templates'

import { TextEditor } from '../text-editor'
import { TagsEditor } from '../tags-editor'

import UIkit from 'uikit';


class SubjectPage extends Component {
    description = 'Страница редактирования предмета'
    icon = 'ion-edit'

    links = [
        {
            name: 'Предметы',
            url: '/subjects'
        }
    ];

    constructor(props) {
        super(props);

        this.state = {
            subject: null
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;

        this.codename = props.match.params.codename;
    }

    componentDidMount() {
        this.isLoading();
        this.loadSubject(this.codename, this.isLoaded);
    }

    loadSubject(codename, callback) {
        this.AdminService.getSubject(codename)
            .then(subject => {
                this.setState(() => { return { subject, title: subject.name } });
            })
            .then(callback);
    }


    handleNameChange = (value) => {
        this.setState((state) => {
            const subject = state.subject;
            subject.name = value;
            return { subject }
        });
    }

    handleTeacherChange = (value) => {
        this.setState((state) => {
            const subject = state.subject;
            subject.teacher = value;
            return { subject }
        });
    }

    handleAliasesChange = (value) => {
        this.setState((state) => {
            const subject = state.subject;
            subject.aliases = value.map((tag) => tag.text);
            return { subject }
        });
    }

    handleInfoChange = (value) => {
        this.setState((state) => {
            const subject = state.subject;
            subject.info = value;
            return { subject }
        });
    }

    handleFileTitleChange = (key, value) => {
        this.setState((state) => {
            const subject = state.subject;
            if (typeof subject.files[key] === 'undefined') {
                subject.files[key] = { title: '', file_id: '' }
            }
            subject.files[key].title = value.trim();
            subject.files = subject.files.filter((file) => (file.title !== '' || file.file_id !== ''));
            return { subject }
        });
    }

    handleFileIDChange = (key, target) => {
        const value = target.value;

        this.AdminService.getFile(value)
            .then(() => {
                target.classList.remove('uk-form-danger')
            })
            .catch(() => {
                target.classList.add('uk-form-danger')
            });

        this.setState((state) => {
            const subject = state.subject;
            if (typeof subject.files[key] === 'undefined') {
                subject.files[key] = { title: '', file_id: '' }
            }
            subject.files[key].file_id = value.trim();
            subject.files = subject.files.filter((file) => (file.title !== '' || file.file_id !== ''));
            return { subject }
        });
    }

    handleSubmit = (e) => {
        e.preventDefault();
        this.isLoading();

        const { subject } = this.state;

        const params = {
            name: subject.name,
            aliases: subject.aliases,
            teacher: subject.teacher,
            info: subject.info,
            files: subject.files
        };

        this.AdminService.editSubject(subject.codename, params)
            .then(subject => {
                this.setState(() => { return { subject, title: subject.name } });
            })
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
        const { title, subject } = this.state;

        if (!subject) {
            return '';
        }

        let showNewFileInput = false;
        if (subject.files.length < 1) {
            showNewFileInput = true;
        } else {
            const lastFile = subject.files.slice(-1).pop();

            if (typeof lastFile !== 'undefined' && lastFile.title !== '' && lastFile.file_id !== '')
                showNewFileInput = true;
        }

        return (
            <PageTemplate title={title} description={this.description} icon={this.icon} links={this.links}>
                <div className="uk-container uk-section-default uk-section-small">

                    <div className="uk-form-stacked" >
                        <div className="uk-margin">
                            <label className="uk-form-label" htmlFor="name">Название</label>
                            <div className="uk-form-controls">
                                <input className="uk-input" id="name" type="text" placeholder="Название пердмета" value={subject ? subject.name : ''} onChange={e => this.handleNameChange(e.target.value)} />
                            </div>
                        </div>

                        <div className="uk-margin">
                            <label className="uk-form-label">Алиасы</label>
                            <div className="uk-form-controls">
                                <TagsEditor onChange={this.handleAliasesChange} placeholder='Введите новый алиас' value={subject ? subject.aliases : ''} />
                            </div>
                            <span className='uk-text-meta'>Дополнительные названия предмета для улучшения распознавания</span>
                        </div>

                        <div className="uk-margin">
                            <label className="uk-form-label" htmlFor="teacher">Учитель</label>
                            <div className="uk-form-controls">
                                <input className="uk-input" id="teacher" type="text" placeholder="Имя учителя" value={subject ? subject.teacher : ''} onChange={e => this.handleTeacherChange(e.target.value)} />
                            </div>
                        </div>

                        <div className="uk-margin">
                            <label className="uk-form-label">Информация</label>
                            <div className="uk-form-controls">
                                <TextEditor onChange={this.handleInfoChange} value={subject ? subject.info : ''} />
                            </div>
                        </div>


                        <div className="uk-margin">
                            <label className="uk-form-label">Документы</label>

                            <div className="uk-margin">
                                {subject.files ? subject.files.map((file, i) =>
                                    <div className="uk-grid-small" uk-grid="true" key={i}>
                                        <div className="uk-width-1-2@s">
                                            <input className="uk-input" type="text" placeholder="Название документа" value={file.title} onChange={e => this.handleFileTitleChange(i, e.target.value)} />
                                        </div>
                                        <div className="uk-width-1-2@s">
                                            <input className="uk-input" type="text" placeholder="ID документа" value={file.file_id} onChange={e => this.handleFileIDChange(i, e.target)} />
                                        </div>
                                    </div>
                                ) : ''}

                                {showNewFileInput &&
                                    <div className="uk-grid-small" uk-grid="true" key={subject.files.length}>
                                        <div className="uk-width-1-2@s">
                                            <input className="uk-input" type="text" placeholder="Название документа" onChange={e => this.handleFileTitleChange(subject.files.length, e.target.value)} />
                                        </div>
                                        <div className="uk-width-1-2@s">
                                            <input className="uk-input" type="text" placeholder="ID документа" onChange={e => this.handleFileIDChange(subject.files.length, e.target)} />
                                        </div>
                                    </div>
                                }

                                <span className="uk-text-meta">Чтобы получить ID документа, отправьте боту команду /get_file_id</span>

                            </div>
                        </div>

                        <button className="uk-button uk-button-primary uk-button-large" onClick={this.handleSubmit}>Сохранить</button>
                    </div>
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(SubjectPage));