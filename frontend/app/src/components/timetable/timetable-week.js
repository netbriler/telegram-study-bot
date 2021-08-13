import React from 'react';

import TimetableDay from './timetable-day';


export default function TimetableWeek({ timetable }) {
    return (
        <div className="uk-card uk-card-default uk-card-body">
            <div className="timetable__week-container">
                {timetable.map((day, i) => (
                    <TimetableDay key={i} day={day} />
                ))}
            </div>
            <hr style={{marginTop:0}}/>
            <a className="uk-button uk-button-text uk-align-right" href="">Сохранить</a>
        </div>

    )

}