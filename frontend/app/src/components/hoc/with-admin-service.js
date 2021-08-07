import AdminServiceContext from '../admin-service-context';
import React from 'react';

const WithAdminService = () => (Wrapped) => { 
    return (props) => {  
        return (
            <AdminServiceContext.Consumer>
                {
                    (AdminService) => {
                        return <Wrapped {...props} AdminService = {AdminService}/>
                    }
                }
            </AdminServiceContext.Consumer>
        )
    }
};

export default WithAdminService;
