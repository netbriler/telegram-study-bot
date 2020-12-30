const isLoading = () => {
    return {
        type: "SHOW_LOADER",
    };
};

const isLoaded = () => {
    return {
        type: "HIDE_LOADER"
    }
}

export {
    isLoading,
    isLoaded
};