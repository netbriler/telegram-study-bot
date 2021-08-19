import React from 'react'
import { Link } from "react-router-dom";

export default function PageTemplate({ title, links = [], description, children, icon }) {

    let breadcrumb = '';

    breadcrumb = links.map((link, i) => (
        <li key={i}><Link to={link.url}>{link.name}</Link></li>
    ))

    return (
        <>
            <div className="content-padder content-background">
                <div className="uk-section-small uk-section-default header">
                    <div className="uk-container">
                        <h1><span className={icon} /> {title}</h1>

                        <p>{description}</p>

                        <ul className="uk-breadcrumb">
                            <li><Link to="/">Главная</Link></li>
                            {breadcrumb}
                            <li><span>{title}</span></li>
                        </ul>
                    </div>
                </div>
                <div className="uk-section-small">
                    {children}
                </div>
            </div>
        </>
    )
}