import React from 'react';

import ReactDOM from "react-dom";
import { Droppable, Draggable } from "react-beautiful-dnd";

export default function TimetableDay({ day }) {
    return (
        <div key={day.day_id} className="timetable__day">
            <h3>
                {day.day_name}
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
                                        >
                                            {subject.content}
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

// export default function TimetableDay({ day }) {
//     return (
//         <div key={day.day_id} className="timetable__day">
//             <h3>
//                 {day.day_name}
//             </h3>
//             <Droppable droppableId={`${day.day_id}`}>
//                 {(provided, snapshot) => (
//                     <div
//                         className="timetable__subjects"
//                         ref={provided.innerRef}
//                         style={getListStyle(snapshot.isDraggingOver)}
//                         {...provided.droppableProps}
//                     >

//                         {day.subjects.map((subject, index) => (
//                             <Draggable
//                                 key={subject.id}
//                                 draggableId={subject.id}
//                                 index={index}
//                             >
//                                 {(provided, snapshot) => (
//                                     <div
//                                         ref={provided.innerRef}
//                                         {...provided.draggableProps}
//                                         {...provided.dragHandleProps}
//                                     >
//                                         {subject.content}
//                                     </div>
//                                 )}
//                             </Draggable>
//                         ))}
//                         {provided.placeholder}
//                     </div>
//                 )}
//             </Droppable>
//         </div>
//     )

// }