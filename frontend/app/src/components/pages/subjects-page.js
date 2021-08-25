import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from "react-router-dom";

import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';
import { PageTemplate } from '../page-templates'

class SubjectsPage extends Component {
    title = 'Предметы'
    description = 'Список всех предметов'
    icon = 'ion-android-list'

    constructor(props) {
        super(props);

        this.state = {
            subjects: []
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.loadSubjects(this.isLoaded);
    }

    loadSubjects(callback) {
        this.AdminService.getAllSubjects()
            .then(subjects => {
                this.setState(() => { return { subjects } });
            })
            .finally(callback);
    }

    render() {
        const { subjects } = this.state;

        let subjects_list_elements = '';

        if (subjects) {
            subjects_list_elements = subjects.map((subject, i) => (
                <div key={i}>
                    <div className="uk-card uk-card-default uk-card-body uk-card-hover">
                        <div className="uk-grid-small uk-flex-middle" uk-grid='true'>
                            <div className="uk-width-expand">
                                <h3 className="uk-card-title uk-margin-remove-bottom">{subject.name}</h3>
                                <p className="uk-text-meta uk-margin-remove-top"><time dateTime="2016-04-01T19:00">{subject.teacher}</time></p>
                            </div>
                        </div>
                        <hr />
                        <Link to={'/subject/' + subject.codename} className="uk-button uk-button-text">Редактировать</Link>
                    </div>
                </div>
            ))
        } else {
            subjects_list_elements = 'Не удалось загрузить предметы';
        }


        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <Link to='/subjects/new' className="uk-button uk-align-center">Создать новый предмет <span className="ion-plus"></span></Link>
                <div className="uk-container uk-container-large">
                    <div uk-grid="true" className="uk-child-width-1-1@s uk-child-width-1-2@m uk-child-width-1-4@xl uk-grid">
                        {subjects_list_elements}
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(SubjectsPage));