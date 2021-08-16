import React, { useState } from 'react';
import { connect } from 'react-redux';

import SelectSearch, { fuzzySearch } from 'react-select-search';

const ChooseModal = ({ modal, target, title, subjects, onChoose }) => {
    const [subjectCodename, setSubject] = useState();

    const options = subjects.map(subject => {
        return {
            name: subject.name,
            value: subject.codename
        }
    }
    );

    const onModalConfirm = () => {
        const selectedSubject = subjects.find(s => {
            return s.codename === subjectCodename
        })

        if (selectedSubject !== undefined) {
            onChoose(selectedSubject)
        }
    }

    return (
        <div id={target} uk-modal={modal.toString()}>
            <div className="uk-modal-dialog uk-modal-body">
                <h2 className="uk-modal-title">{title}</h2>
                <ul className="uk-list uk-list-divider">
                    <SelectSearch
                        options={options}
                        search
                        filterOptions={fuzzySearch}
                        emptyMessage="Не найдено"
                        placeholder="Выбери предмет"
                        onChange={setSubject}
                    />
                </ul>
                <p className="uk-text-right">
                    <button className="uk-button uk-button-primary uk-modal-close" type="button" onClick={onModalConfirm}>Ок</button>
                    <button className="uk-button uk-button-default uk-modal-close" type="button">Отменить</button>
                </p>
            </div>
        </div>
    )
};

export default ChooseModal;