const isLoading = () => {
    return {
        type: 'SHOW_LOADER',
    };
};

const isLoaded = () => {
    return {
        type: 'HIDE_LOADER'
    }
}

const setCurrentUser = (user) => {
    return {
        type: 'SET_CURRENT_USER',
        payload: user
    }
}

export {
    isLoading,
    isLoaded,
    setCurrentUser
};