import React, { Component } from 'react';
import { connect } from 'react-redux';
import { isLoaded, isLoading } from '../../actions';
import WithAdminService from '../hoc';

import { PageTemplate } from '../page-templates'

import ReactDOM from "react-dom";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

import UIkit from 'uikit';


const reorder = (list, startIndex, endIndex) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
};

const move = (source, destination, droppableSource, droppableDestination) => {
    const sourceClone = Array.from(source);
    const destClone = Array.from(destination);
    const [removed] = sourceClone.splice(droppableSource.index, 1);

    destClone.splice(droppableDestination.index, 0, removed);

    const result = {};
    result[droppableSource.droppableId] = sourceClone;
    result[droppableDestination.droppableId] = destClone;

    return result;
};

const getListStyle = isDraggingOver => ({
    background: isDraggingOver ? "lightblue" : "lightgrey",
    padding: 20,
    width: 250
});


class TimetablePage extends Component {
    title = 'Расписание'
    description = 'Страница редактирования расписания'
    icon = 'ion-edit'

    constructor(props) {
        super(props);

        this.state = {
            timetable: null
        }

        this.AdminService = this.props.AdminService;
        this.isLoading = props.isLoading;
        this.isLoaded = props.isLoaded;
    }

    componentDidMount() {
        this.isLoading();
        this.loadTimetable(this.isLoaded);
    }

    loadTimetable(callback) {
        this.AdminService.getTimetable()
            .then(timetable => {
                this.setState(() => {
                    timetable = timetable.map(day => {


                        day.subjects = Object.entries(day.subjects).map(([subjectIndex, subject]) => ({
                            id: `${day.day_id}-${subjectIndex}-${subject.codename}`,
                            content: subject.name,
                            codename: subject.codename
                        }))


                        return day

                        
                    });

                    return { timetable }
                });
            })
            .then(callback);
    }

    onDragEnd = (result) => {
        const { source, destination } = result;
        const { timetable } = this.state;

        // dropped outside the list
        if (!result.destination) {
            return;
        }

        const sInd = +source.droppableId;
        const dInd = +destination.droppableId;

        let newState = [...timetable];

        if (sInd === dInd) {
            const subjects = reorder(
                timetable[dInd].subjects,
                result.source.index,
                result.destination.index
            );
            newState[sInd].subjects = subjects;
        } else {
            const result = move(timetable[sInd].subjects, timetable[dInd].subjects, source, destination);
            newState[sInd].subjects = result[sInd];
            newState[dInd].subjects = result[dInd];
        }

        this.setState({
            timetable: newState
        });
    }

    render() {
        const { timetable } = this.state;

        if (!timetable) {
            return '';
        }

        console.log(timetable)

        return (
            <PageTemplate title={this.title} description={this.description} icon={this.icon}>
                <div className="uk-container uk-container-large uk-section-default">
                    <DragDropContext onDragEnd={this.onDragEnd}>
                        <div className="timetable__container">

                            {timetable.map((day, dayIndex) => (
                                <Droppable key={dayIndex} droppableId={`${dayIndex}`}>
                                    {(provided, snapshot) => (
                                        <div
                                            ref={provided.innerRef}
                                            style={getListStyle(snapshot.isDraggingOver)}
                                            {...provided.droppableProps}
                                        >

                                            <h3>
                                                {day.day_name}
                                            </h3>

                                            {day.subjects.map((subject, index) => (
                                                <Draggable
                                                    key={subject.id}
                                                    draggableId={subject.id}
                                                    index={index}
                                                >
                                                    {(provided, snapshot) => (
                                                        <div
                                                            ref={provided.innerRef}
                                                            {...provided.draggableProps}
                                                            {...provided.dragHandleProps}
                                                        >
                                                            {subject.content}
                                                        </div>
                                                    )}
                                                </Draggable>
                                            ))}
                                            {provided.placeholder}
                                        </div>
                                    )}
                                </Droppable>
                            ))}

                        </div>

                    </DragDropContext>
                </div>
            </PageTemplate>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        loading: state.loading
    }
}


const mapDispatchToProps = {
    isLoaded,
    isLoading
}

export default WithAdminService()(connect(mapStateToProps, mapDispatchToProps)(TimetablePage));