import React, { Component } from 'react';
import { WithContext as ReactTags } from 'react-tag-input';


class TagsEditor extends Component {
    constructor(props) {
        super(props);

        let tags = [];

        if (props.value) {
            props.value.map((tag) => {
                tags.push({ id: tag, text: tag })
            });
        }

        this.state = {
            tags
        }

        this.onChange = props.onChange;
        this.placeholder = props.placeholder ? props.placeholder : '';
    }

    handleDelete = (i) => {
        this.setState(state => {
            const tags = state.tags.filter((tag, index) => index !== i);

            this.onChange(tags);

            return { tags }
        });
    }

    handleAddition = (tag) => {
        this.setState(state => {
            const tags = [...state.tags, tag];

            this.onChange(tags);

            return { tags }
        });
    }

    render() {
        return (
            <>
                <ReactTags tags={this.state.tags}
                    handleDelete={this.handleDelete}
                    handleAddition={this.handleAddition}
                    allowDragDrop={false}
                    autofocus={false}
                    placeholder={this.placeholder} />
            </>
        )
    }
}


export default TagsEditor;