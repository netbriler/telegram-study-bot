import React, {Component} from 'react';
import {connect} from 'react-redux';
import {
    Switch,
    Route,
    Redirect,
} from "react-router-dom";
import Panel from '../panel'
import {DashboardPage, LogPage, SubjectsPage, UsersPage} from '../pages'
import UIkit from 'uikit'
import {isLoaded, isLoading, setCurrentUser} from '../../actions';
import WithAdminService from '../hoc';

class App extends Component {

    constructor(props) {
        super(props);

        this.AdminService = props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
        this.setCurrentUser = props.setCurrentUser;

    }

    componentDidMount() {
        this.isLoading();
        this.init(this.isLoaded);
    }

    init(callback) {
        this.AdminService.getCurrentUser()
            .then(user => {
                if (user) {
                    this.setCurrentUser(user)
                } else {
                    throw new Error('Не плучилось загрузить пользователя')
                }
            })
            .then(callback);
    }

    render() {

        return (
            <>
                <Panel/>
                <Switch>
                    <Route path="/dashboard" component={DashboardPage}></Route>
                    <Route path="/subjects" component={SubjectsPage}></Route>
                    <Route path="/users" component={UsersPage}></Route>
                    <Route path="/log" component={LogPage}></Route>
                    <Redirect from="/" exact to="/dashboard"></Redirect>
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
    isLoading,
    setCurrentUser
}

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(App));