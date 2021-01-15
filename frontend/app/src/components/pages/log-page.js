import React from 'react'
import { PageTemplate } from '../page-templates'

export default function LogPage() {

    const log = '2020-11-16 08:32:19,216 [INFO] [funcs.py:229] callback_id: "4314606423703195190"; message_id: "5286"; from_user: "1004572590"; chat_id: "-1001226445436"; data: "info_gromad"'

    let logs = ''
    for (let i = 0; i < 60; i++) {
        logs += `${log}\n`;

    }

    return (
        <PageTemplate name='Логи' description='Инструмент для разработчиков' icon='ion-clipboard'>
            <div className="uk-container uk-container-large uk-section-default">
                {log}
            </div>
        </PageTemplate>
    )
}