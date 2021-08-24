import React, { useState } from 'react';
import SelectSearch, { fuzzySearch } from 'react-select-search';

export default function EditableSelect({ value, name, options, onChange }) {
    const [isEditing, setEditing] = useState(false);

    const onSelect = (option) => {
        if (option != value) {
            onChange(option);
        }
        setEditing(false);
    }

    return (
        <>
            {isEditing ?

                <SelectSearch
                    className='select-search select-search--small'
                    value={value}
                    options={options}
                    search
                    filterOptions={fuzzySearch}
                    emptyMessage='Не найдено'
                    placeholder='Выберите статус'
                    onChange={onSelect}
                    onBlur={() => setEditing(false)}
                    autoFocus={true}
                    closeOnSelect={true}
                />

                : <span onClick={() => setEditing(true)} style={{ borderBottom: 'dashed 1px #000', cursor: 'pointer' }}>{name}</span>}
        </>
    )
}