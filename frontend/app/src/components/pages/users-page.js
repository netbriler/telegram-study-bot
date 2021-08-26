import React, { Component } from 'react';
import { connect } from 'react-redux';
import UIkit from 'uikit';
import { isLoaded, isLoading } from '../../actions';
import EditableSelect from '../editable-select';
import WithAdminService from '../hoc';
import { PageTemplate } from '../page-templates';


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

        this.currentUser = props.currentUser;
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
            .finally((callback));
    }

    editUserStatus(id, status) {
        this.isLoading();

        const { users } = this.state;

        const params = { status };

        this.AdminService.editUserStatus(id, params)
            .then(editedUser => {
                const editedUsers = users.map(user => user.id == editedUser.id ? editedUser : user);

                this.setState({ users: editedUsers });
            })
            .catch(({ response }) => {
                this.showNotification('Произошла ошибка при изменении', 'danger')
            })
            .finally(this.isLoaded);
    }

    showNotification = (message, status) => {
        UIkit.notification({ message, status });
    }

    render() {
        const { users } = this.state;

        let users_list_elements = '';

        if (users) {
            users_list_elements = users.map((user, i) => {
                let style = {};

                if (['super_admin', 'admin'].includes(user.status)) {
                    style = { background: 'rgb(84 179 71 / 28%)' }
                }

                if (['banned'].includes(user.status)) {
                    style = { background: 'rgb(224 62 26 / 41%)' }
                }

                style.height = 70;

                let canEditUser = this.currentUser.statuses_to_edit.find(s => s.value === user.status) ? true : false;

                return (
                    <tr key={i} style={style}>
                        <td>{user.id}</td>
                        <td><img className="uk-preserve-width uk-border-circle" src={'/static/pictures/' + (user.photo_id ? user.photo_id + '.jpg' : 'default-avatar.png')} width="40" alt="" /></td>
                        <td>{user.name}</td>
                        <td>
                            {user.username ? <a href={'https://t.me/' + user.username}>@{user.username}</a> : <span className='uk-text-meta'>Не указан</span>}
                        </td>
                        <td style={{ width: 190 }}>
                            {this.currentUser.id != user.id && canEditUser ? <EditableSelect value={user.status} name={user.status_title} options={this.currentUser.statuses_to_edit} onChange={(status) => this.editUserStatus(user.id, status)} /> : user.status_title}
                        </td>
                    </tr>

                )
            })
        } else {
            users_list_elements = 'Не удалось загрузить пользователей';
        }


        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container uk-section-default" style={{ overflow: 'scroll' }}>
                    <table className="uk-table uk-table-middle uk-table-divider">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Аватарка</th>
                                <th>Имя Фамилия</th>
                                <th>Логин</th>
                                <th>Статус</th>
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