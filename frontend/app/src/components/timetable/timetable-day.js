import React from 'react';

import ReactDOM from "react-dom";
import { Droppable, Draggable } from "react-beautiful-dnd";

export default function TimetableDay({ day, deleteSubject }) {
    return (
        <div key={day.day_id} className="timetable__day">
            <h3>
                {day.day_name} <span className="ion-plus"></span>
            </h3>
            <Droppable droppableId={`${day.day_id}`}>
                {(provided, snapshot) => (
                    <div
                        className="timetable__subjects"
                        ref={provided.innerRef}
                        {...provided.droppableProps}
                    >
                        <ul className="uk-list uk-list-decimal">
                            {day.subjects.map((subject, index) => (
                                <Draggable
                                    key={subject.id}
                                    draggableId={subject.id}
                                    index={index}
                                >
                                    {(provided, snapshot) => (
                                        <li
                                            ref={provided.innerRef}
                                            {...provided.draggableProps}
                                            {...provided.dragHandleProps}
                                            onMouseEnter={e => {
                                                document.querySelector(`[data-rbd-draggable-id="${subject.id}"] > span.ion-android-delete`).style.display = '';
                                            }}
                                            onMouseLeave={e => {
                                                document.querySelector(`[data-rbd-draggable-id="${subject.id}"] > span.ion-android-delete`).style.display = 'none';
                                            }}
                                        >
                                            {subject.content} <span className="ion-android-delete trash-icon" style={{ display: 'none', cursor: 'pointer' }} onClick={() => deleteSubject(day.day_id, index)}></span>
                                            {provided.placeholder}
                                        </li>
                                    )}
                                </Draggable>

                            ))}
                        </ul>
                    </div>
                )}
            </Droppable>


        </div>
    )

}
