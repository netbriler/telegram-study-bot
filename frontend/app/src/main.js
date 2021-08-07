import { BrowserRouter as Router, } from "react-router-dom";
import { Provider } from 'react-redux';
import AdminService from './services/admin-service';
import AdminServiceContext from './components/admin-service-context';
import App from './components/app';
import ErrorBoundry from './components/error-boundry';
import React from 'react';
import ReactDOM from 'react-dom';
import Spinner from './components/spinner';
import store from './store';

ReactDOM.render(
    <Provider store={store}>
        <ErrorBoundry>
            <AdminServiceContext.Provider value={AdminService}>
                <Spinner />
                <Router>
                    <App />
                </Router>
            </AdminServiceContext.Provider>
        </ErrorBoundry>
    </Provider>
    , document.getElementById('root'));