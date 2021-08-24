import React from 'react'

import { PageTemplate } from '../page-templates'

export default function LogPage() {
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