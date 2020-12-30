import React from 'react'

export default function LogPage() {

    const log = '2020-11-16 08:32:19,216 [INFO] [funcs.py:229] callback_id: "4314606423703195190"; message_id: "5286"; from_user: "1004572590"; chat_id: "-1001226445436"; data: "info_gromad"'

    let logs = ''
    for (let i = 0; i < 60; i++) {
        logs += `${log}\n`;

    }

    return (
        <>
            <div className="content-padder content-background">
                <div className="uk-section-small uk-section-default header">
                    <div className="uk-container uk-container-large">
                        <h1><span className="ion-clipboard"/> Логи</h1>

                        <p>Инструмент для разработчиков</p>

                        <ul className="uk-breadcrumb">
                            <li><a href="#">Главная</a></li>
                            <li><span href="#">Логи</span></li>
                        </ul>
                    </div>
                </div>
                <div className="uk-section-small">
                    <div className="uk-container uk-container-large">
                        <pre>{logs}</pre>
                    </div>
                </div>
            </div>
        </>
    )
}