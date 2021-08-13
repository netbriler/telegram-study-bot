import React from 'react';

import ReactDOM from "react-dom";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

import TimetableWeek from './timetable-week';

export default function Timetable({ onDragEnd, timetable }) {
    return (
        <DragDropContext onDragEnd={onDragEnd}>
            <div className='timetable__container'>
                <TimetableWeek timetable={timetable.slice(0, 6)} />
                <TimetableWeek timetable={timetable.slice(7, 13)} />
            </div>
        </DragDropContext>
    )

}