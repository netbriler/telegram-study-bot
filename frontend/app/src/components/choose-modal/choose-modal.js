import React, { useState } from 'react';
import SelectSearch, { fuzzySearch } from 'react-select-search';

const ChooseModal = ({ modal, target, title, subjects, onChoose }) => {
    const [subjectCodename, setSubject] = useState(null);

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
            onChoose(selectedSubject);
            setSubject(null);
        }
    }

    return (
        <div id={target} uk-modal={modal.toString()}>
            <div className="uk-modal-dialog uk-modal-body">
                <h2 className="uk-modal-title">{title}</h2>
                <ul className="uk-list uk-list-divider">
                    <SelectSearch
                        className="select-search uk-input"
                        value={subjectCodename}
                        options={options}
                        search
                        filterOptions={fuzzySearch}
                        emptyMessage="Не найдено"
                        placeholder="Выберите предмет"
                        onChange={setSubject}
                        autoFocus={true}
                    />
                </ul>
                <p className="uk-text-right">
                    <button className="uk-button uk-button-primary uk-modal-close" type="button" onClick={onModalConfirm}>Ок</button>
                </p>
            </div>
        </div>
    )
};

export default ChooseModal;