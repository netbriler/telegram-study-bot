import React from 'react';

import AdminServiceContext from '../admin-service-context';

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
