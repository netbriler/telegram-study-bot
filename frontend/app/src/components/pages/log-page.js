import React from 'react'
import { PageTemplate } from '../page-templates'

export default function LogPage() {

    const log = '2020-11-16 08:32:19,216 [INFO] [funcs.py:229] callback_id: "4314606423703195190"; message_id: "5286"; from_user: "1004572590"; chat_id: "-1001226445436"; data: "info_gromad"'

    let logs = ''
    for (let i = 0; i < 60; i++) {
        logs += `${log}\n`;

    }

    return (
        <PageTemplate title='Логи' description='Инструмент для разработчиков' icon='ion-clipboard'>
            <iframe src="/logs" frameBorder={0} style={{ border: 0, width: '100%', height: '100%' }} onLoad={(e) => {
                e.target.style.height = 0;
                e.target.style.height = e.target.contentWindow.document.body.scrollHeight + 50 + 'px';

                setTimeout(() => window.scrollTo(0,document.body.scrollHeight), 100);
            }}></iframe>
        </PageTemplate>
    )
}