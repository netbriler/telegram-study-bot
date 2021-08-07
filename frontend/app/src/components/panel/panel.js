import React from 'react';
import { Link } from "react-router-dom";
import { connect } from 'react-redux';

const Panel = ({user}) => {
    return (
        <>
            <div uk-sticky="true" className="uk-navbar-container tm-navbar-container uk-sticky uk-sticky-fixed" style={{ position: 'fixed', top: '0px', width: '100%' }}>
                <div className="uk-container uk-container-expand">
                    <nav uk-navbar="true" className="uk-navbar">
                        <div className="uk-navbar-left">
                            <a id="sidebar_toggle" className="uk-navbar-toggle uk-navbar-toggle-icon uk-icon" uk-navbar-toggle-icon="true"><svg width={20} height={20} viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" data-svg="navbar-toggle-icon"><rect y={9} width={20} height={2} /><rect y={3} width={20} height={2} /><rect y={15} width={20} height={2} /></svg></a>
                            <a href="#" className="uk-navbar-item uk-logo">
                                Briler Admin
                </a>
                        </div>
                        <div className="uk-navbar-right uk-light">
                            <ul className="uk-navbar-nav">
                                <li className="uk-active">
                                    <a href="#" aria-expanded="false">{user.name} &nbsp;<span className="ion-ios-arrow-down" /></a>
                                    <div uk-dropdown="pos: bottom-right; mode: click; offset: -17;" className="uk-dropdown">
                                        <ul className="uk-nav uk-navbar-dropdown-nav">
                                            <li className="uk-nav-header">Настройки</li>
                                            <li><a href="#">Edit Profile</a></li>
                                            <li className="uk-nav-header">Actions</li>
                                            <li><a href="/logout">Logout</a></li>
                                        </ul>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>
            </div>
            <div id="sidebar" className="tm-sidebar-left uk-background-default">
                <center>
                    <div className="user">
                        <img id="avatar" width={100} className="uk-border-circle" src={'/static/pictures/' + (user.photo_id ? user.photo_id+'.jpg' : 'default-avatar.png')} />
                        <div className="uk-margin-top" />
                        <div id="name" className="uk-text-truncate">{user.name}</div>
                        <div id="email" className="uk-text-truncate">{user.username ? <a href={'https://t.me/' + user.username}>@{user.username}</a> : <span className='uk-text-meta'>Не указан</span>}</div>
                        <span id="status" data-enabled="true" data-online-text="Online" data-away-text="Away" data-interval={10000} className="uk-margin-top uk-label uk-label-danger">{user.status}</span>
                    </div>
                    <br />
                </center>
                <ul className="uk-nav uk-nav-default">
                    <li className="uk-nav-header">
                        Основное
            </li>
                    <li><Link to="/subjects">Предметы</Link></li>
                    <li><Link to="/users">Пользователи</Link></li>
                    <li><a href="#">Домашние задания</a></li>
                    <li className="uk-nav-header">
                        Дополнительное
            </li>
                    <li><a href="#">Переписка</a></li>
                    <li><a href="#">Рассылка</a></li>
                    <li><Link to="/log">Логи</Link></li>
                </ul>
            </div>
        </>
    )
};


const mapStateToProps = (state) => {
    return {
        user: state.user
    }
}

export default connect(mapStateToProps)(Panel);