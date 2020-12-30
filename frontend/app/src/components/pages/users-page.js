import React from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';

function UsersPage({isLoaded}) {
    isLoaded();

    return (
        <>
            <div className="content-padder content-background">
                <div className="uk-section-small uk-section-default header">
                    <div className="uk-container uk-container-large">
                        <h1><span className="ion-android-people" /> Пользователи</h1>

                        <p>Список всех пользователей бота</p>

                        <ul className="uk-breadcrumb">
                            <li><a href="#">Главная</a></li>
                            <li><span href="#">Пользователи</span></li>
                        </ul>
                    </div>
                </div>
                <div className="uk-section-small">
                    <div className="uk-container uk-container-large uk-section-default">
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
                                {[0, 1, 2, 3, 4].map((value, i) => (
                                <tr key={i}>
                                    <td><img className="uk-preserve-width uk-border-circle" src="https://avatars3.githubusercontent.com/u/44978350?s=460&u=93bc67a53a2046f63c927523772c59979d3bb3c9&v=4" width="40" alt="" /></td>
                                    <td>@briler</td>
                                    <td>Yaroslav Logger</td>
                                    <td>243823495</td>
                                    <td>Super Admin</td>
                                    <td>
                                        <p uk-margin="true">
                                            <button className="uk-button uk-button-default" type="button" style={{ marginRight: 8 }}>Редактировать</button><button className="uk-button uk-button-danger" type="button">Удалить</button>
                                        </p>
                                    </td>
                                </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </>
    )
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