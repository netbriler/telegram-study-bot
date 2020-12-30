import React, { Component } from 'react';
import {
    Switch,
    Route,
    Redirect,
} from "react-router-dom";
import Panel from '../panel'
import { DashboardPage, LogPage, SubjectsPage, UsersPage } from '../pages'
import UIkit from 'uikit'

class App extends Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <>
                <Panel />
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

export default App;