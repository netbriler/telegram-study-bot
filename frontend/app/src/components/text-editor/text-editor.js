import React, { Component } from 'react';
import ReactQuill from 'react-quill';

import 'react-quill/dist/quill.snow.css';

class TextEditor extends Component {
    constructor(props) {
        super(props);

        this.state = {
            text: props.value ? props.value.replaceAll(/(.+)\r?\n/gm, '<p>$1</p>') : ''
        }

        this.onChange = props.onChange;
    }

    
    componentDidUpdate(prevProps) {
        if (this.props.text !== prevProps.text) {
            this.setState({ text: this.props.text });
        }
    }

    handleChange = (value) => {
        this.setState({ text: value });

        const formatedText = value.replaceAll(/(<a href="[^"]+")([^>]+)(>)/gm, '$1$3').replaceAll(/<p>/gm, '').replaceAll(/<\/p>|<br>|<\/br>/gm, '\n').replaceAll(/(<pre)([^>]+)(>)/gm, '$1$3');

        this.onChange(formatedText);
    }

    modules = {
        toolbar: [
            ['bold', 'italic', 'strike', 'underline'],
            ['link', 'code-block']
        ],
    }

    formats = [
        'bold', 'italic', 'underline', 'strike',
        'link', 'code-block'
    ]

    render() {
        return (
            <>
                <ReactQuill value={this.state.text}
                    onChange={this.handleChange}
                    modules={this.modules}
                    formats={this.formats} />
            </>
        )
    }
}


export default TextEditor;