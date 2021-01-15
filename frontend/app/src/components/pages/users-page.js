import React, { Component } from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';

import { PageTemplate } from '../page-templates'

class UsersPage extends Component {
    title = 'Пользователи'
    description = 'Список всех пользователей бота'
    icon = 'ion-android-people'

    constructor(props) {
        super(props);

        this.state = {
            users: []
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.loadUsers(this.isLoaded);
    }

    loadUsers(callback) {
        this.AdminService.getAllUsers()
            .then(users => {
                this.setState(() => { return { users } });
            })
            .then(callback);
    }

    render() {
        const { users } = this.state;

        let users_list_elements = '';

        if (users) {
            users_list_elements = users.map((user, i) => (
                <tr key={i}>
                    <td><img className="uk-preserve-width uk-border-circle" src={'/static/pictures/' + (user.photo_id ? user.photo_id + '.jpg' : 'default-avatar.png')} width="40" alt="" /></td>
                    <td>
                        {user.username ? <a href={'https://t.me/' + user.username}>@{user.username}</a> : <span className='uk-text-meta'>Не указан</span>}
                    </td>
                    <td>{user.name}</td>
                    <td>{user.id}</td>
                    <td>{user.status}</td>
                    <td>
                        <p uk-margin="true">
                            <button className="uk-button uk-button-default" type="button" style={{ marginRight: 8 }}>Редактировать</button><button className="uk-button uk-button-danger" type="button">Удалить</button>
                        </p>
                    </td>
                </tr>
            ))
        } else {
            users_list_elements = 'Не удалось загрузить предметы';
        }


        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container uk-section-default">
                    <table className="uk-table uk-table-middle uk-table-divider">
                        <thead>
                            <tr>
                                <th>Аватарка</th>
                                <th>Логин</th>
                                <th>Имя Фамилия</th>
                                <th>ID</th>
                                <th>Статус</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users_list_elements}
                        </tbody>
                    </table>
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

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(UsersPage));