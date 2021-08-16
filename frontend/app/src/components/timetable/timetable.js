import React from 'react';

import { DragDropContext } from "react-beautiful-dnd";

import TimetableWeek from './timetable-week';


export default function Timetable({ onDragEnd, timetable, deleteSubject, subjects, addSubject }) {
    return (
        <>
            <DragDropContext onDragEnd={onDragEnd}>
                <div className='timetable__container'>
                    <TimetableWeek timetable={timetable.slice(0, 6)} deleteSubject={deleteSubject} addSubject={addSubject} subjects={subjects}/>
                    <TimetableWeek timetable={timetable.slice(7, 13)} deleteSubject={deleteSubject} addSubject={addSubject} subjects={subjects}/>
                </div>
            </DragDropContext>
        </>
    )

}