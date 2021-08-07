const initialState = {
    loading: true,
    user: []
}


const reducer = (state = initialState, action) => {
    switch (action.type) {
        case 'SHOW_LOADER':
            return {
                ...state,
                loading: true,
            };
        case 'HIDE_LOADER':
            return {
                ...state,
                loading: false
            };
        case 'SET_CURRENT_USER':
            const user = action.payload;
            return {
                ...state,
                user
            }
        default:
            return state;
    }
}

export default reducer;