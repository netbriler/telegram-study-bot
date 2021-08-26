import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Redirect, Route, Switch } from "react-router-dom";

import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';
import { HomeworkPage, LogPage, SubjectPage, SubjectsPage, TimetablePage, UsersPage } from '../pages';
import Panel from '../panel';

class App extends Component {

    constructor(props) {
        super(props);

        this.state = {
            currentUser: null
        }

        this.AdminService = props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.init(this.isLoaded);
    }

    init(callback) {
        this.AdminService.getCurrentUser()
            .then(currentUser => {
                if (currentUser) {
                    this.setState({ currentUser })
                } else {
                    throw new Error('Не плучилось загрузить пользователя')
                }
            })
            .finally(callback);
    }

    render() {
        if (!this.state.currentUser) {
            return ''
        }

        return (
            <>
                <Panel currentUser={this.state.currentUser} />
                <Switch>
                    <Route path="/subjects/new" component={SubjectPage}></Route>
                    <Route path="/subject/:codename" component={SubjectPage}></Route>
                    <Route path="/subjects" component={SubjectsPage}></Route>

                    <Route path="/timetable" component={TimetablePage}></Route>

                    <Route
                        path='/users'
                        render={(props) => (
                            <UsersPage {...props} currentUser={this.state.currentUser} />
                        )}
                    />

                    <Route path="/homework/:id" component={HomeworkPage}></Route>
                    <Route path="/homework" component={HomeworkPage}></Route>

                    <Route path="/log" component={LogPage}></Route>
                    <Redirect from="*" exact to="/subjects"></Redirect>
                </Switch>
            </>
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(App));