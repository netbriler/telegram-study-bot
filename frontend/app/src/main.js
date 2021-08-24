import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { BrowserRouter as Router } from "react-router-dom";

import AdminServiceContext from './components/admin-service-context';
import App from './components/app';
import ErrorBoundry from './components/error-boundry';
import Spinner from './components/spinner';
import AdminService from './services/admin-service';
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