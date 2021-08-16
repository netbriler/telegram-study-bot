import React from 'react';

import { Droppable, Draggable } from "react-beautiful-dnd";

import UIkit from 'uikit';

import ChooseModal from '../choose-modal';


function TimetableDay({ day, deleteSubject, addSubject, subjects }) {
    const modal = true;

    const toggleModal = () => {
        UIkit.modal(`#modal-subjects-day-${day.day_id}`).toggle()
    }

    const onSubjectSelected = (subject) => {
        addSubject(day, subject)
    }

    return (
        <div key={day.day_id} className="timetable__day">
            <h3>
                {day.day_name} <span className="ion-plus" onClick={toggleModal}></span>
            </h3>
            <Droppable droppableId={`${day.day_id}`} isUsingPlaceholder={false}>
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
                                        </li>
                                    )}
                                </Draggable>
                            ))}
                        </ul>
                        <div style={{ display: 'none' }}>{provided.placeholder}</div>
                    </div>
                )}
            </Droppable>
            <ChooseModal modal={modal} target={`modal-subjects-day-${day.day_id}`} onChoose={onSubjectSelected} subjects={subjects} addSubject={addSubject} />
        </div>
    )

}

export default TimetableDay;