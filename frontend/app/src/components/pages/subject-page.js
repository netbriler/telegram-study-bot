import React, { Component } from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';
import { Redirect } from "react-router-dom";

import { PageTemplate } from '../page-templates'

import { TextEditor } from '../text-editor'
import { TagsEditor } from '../tags-editor'

import UIkit from 'uikit';
import CyrillicToTranslit from 'cyrillic-to-translit-js';

const cyrillicToTranslit = new CyrillicToTranslit();

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
            subject: null,
            is_new: false,

            errors: {
                name: false,
                codename: false
            }
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;

        this.codename = props.match.params.codename;
    }

    componentDidMount() {
        if (this.codename != null) {
            this.isLoading();
            this.loadSubject(this.codename, this.isLoaded);
        } else {
            this.setState(() => {
                return {
                    subject: {
                        audience: '',
                        codename: '',
                        aliases: [],
                        files: [{ title: '', file_id: '' }],
                        info: '',
                        name: '',
                        teacher: '',
                    }, title: 'Новый предмет', is_new: true
                }
            });
            this.description = 'Страница создания предмета'
        }
    }

    loadSubject(codename, callback) {
        this.AdminService.getSubject(codename)
            .then(subject => {
                if (subject == null) {
                    this.props.history.push('/subjects')
                }
                subject.files.push({ title: '', file_id: '' });
                this.setState(() => { return { subject, title: subject.name } });
            })
            .then(callback);
    }

    _formatCodename(codename) {
        return cyrillicToTranslit.transform(codename.trim(), '_').toLowerCase().replace(/[^_0-9a-z]/gi, '');
    }

    handleCodenameChange = (value) => {
        this.setState((state) => {
            const { subject, errors } = state;
            if (state.is_new) {
                subject.codename = this._formatCodename(value);
                errors.codename = value.trim() == '';
            }

            return { subject, errors }
        });
    }

    handleNameChange = (value) => {
        this.setState((state) => {
            const { subject, errors } = state;

            subject.name = value;
            errors.name = value.trim() == '';

            if (state.is_new) {
                subject.codename = this._formatCodename(value);
                errors.codename = subject.codename == '';
            }

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

    handleAudienceChange = (value) => {
        this.setState((state) => {
            const subject = state.subject;
            subject.audience = value;
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
            subject.files.push({ title: '', file_id: '' });
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
            subject.files.push({ title: '', file_id: '' });
            return { subject }
        });
    }

    handleEditSubmit = (e) => {
        e.preventDefault();

        if (this.state.errors.name || this.state.errors.codename) {
            return this.showNotification('Заполните все обязательные поля!', 'danger')
        }

        this.isLoading();

        const { subject } = this.state;

        const params = {
            name: subject.name,
            aliases: subject.aliases,
            teacher: subject.teacher,
            audience: subject.audience,
            info: subject.info,
            files: subject.files.filter((file) => (file.title !== '' || file.file_id !== ''))
        };

        this.AdminService.editSubject(subject.codename, params)
            .then(subject => {
                subject.files.push({ title: '', file_id: '' });
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

    handleDelete = (e) => {
        e.preventDefault();
        const { subject } = this.state;

        UIkit.modal.confirm('Вы точно хотите удалить предмет?', { labels: { ok: 'Да', cancel: 'Отмена' }, stack: true })
            .then(() => {
                this.AdminService.deleteSubject(subject.codename)
                .then(() => {
                    this.setState(() => { return { redirect: true } });
                })
                .then(this.isLoaded)
                .catch(({ response }) => {
                    this.showNotification('Произошла ошибка при удалении', 'danger')
                });
            }, () => {});
    }

    handleCreateSubmit = (e) => {
        e.preventDefault();

        if (this.state.errors.name || this.state.errors.codename) {
            return this.showNotification('Заполните все обязательные поля!', 'danger')
        }

        this.isLoading();

        const { subject } = this.state;

        const params = {
            codename: subject.codename,
            name: subject.name,
            aliases: subject.aliases,
            teacher: subject.teacher,
            audience: subject.audience,
            info: subject.info,
            files: subject.files.filter((file) => (file.title !== '' || file.file_id !== ''))
        };

        this.AdminService.createSubject(params)
            .then((response) => {
                if (response.status == 409) {
                    this.setState(({ errors }) => {
                        errors.codename = true;
                        return { errors }
                    });
                    return this.showNotification('Предмет с таким кодовым именем уже существует', 'danger')
                }
                this.setState(() => { return { redirect: true } });
            })
            .then(this.isLoaded)
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при создании', 'danger')
            });

        this.isLoaded();
    }

    showNotification = (message, status) => {
        UIkit.notification({ message, status });
    }

    render() {
        const { is_new, title, subject, errors, redirect } = this.state;

        if (!subject) {
            return '';
        }

        if (redirect) {
            return <Redirect to={'/subjects'} />;
        }

        return (
            <PageTemplate title={title} description={this.description} icon={this.icon} links={this.links}>
                <div className="uk-container uk-section-default uk-section-small">

                    <div className="uk-form-stacked" >
                        <div className="uk-margin">
                            <label className="uk-form-label" htmlFor="name">Название*</label>
                            <div className="uk-form-controls">
                                <input className={
                                    errors.name ? 'uk-input uk-form-danger' : 'uk-input'
                                } id="name" type="text" autoFocus required placeholder="Название пердмета" value={subject ? subject.name : ''} onChange={e => this.handleNameChange(e.target.value)} />
                            </div>
                        </div>

                        {is_new &&
                            <div className="uk-margin">
                                <label className="uk-form-label" htmlFor="codename">Уникальное кодовое имя*</label>
                                <div className="uk-form-controls">
                                    <input className={
                                        errors.codename ? 'uk-input uk-form-danger' : 'uk-input'
                                    } id="codename" type="text" required placeholder="Уникальное кодовое имя" value={subject ? subject.codename : ''} onChange={e => this.handleCodenameChange(e.target.value)} />
                                </div>
                            </div>
                        }

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
                            <label className="uk-form-label" htmlFor="audience">Аудитория</label>
                            <div className="uk-form-controls">
                                <input className="uk-input" id="audience" type="text" placeholder="Номер аудитории" value={subject ? subject.audience : ''} onChange={e => this.handleAudienceChange(e.target.value)} />
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

                                <span className="uk-text-meta">Чтобы получить ID документа, отправьте боту команду /get_file_id</span>

                            </div>
                        </div>


                        {is_new ?
                            <button className="uk-button uk-button-primary uk-button-large" onClick={this.handleCreateSubmit}>Создать</button> :
                            <>
                                <button className="uk-button uk-button-primary uk-button-large" onClick={this.handleEditSubmit}>Сохранить</button>
                                <button className="uk-button uk-button-danger uk-button-large" onClick={this.handleDelete} style={{ marginLeft: 10 }}>Удалить</button>
                            </>
                        }
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