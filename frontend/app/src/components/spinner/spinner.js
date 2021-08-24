import React from 'react';
import { connect } from 'react-redux';

const Spinner = ({ loading }) => {
    return (
        <>
            <div className={loading ? 'spinner active' : 'spinner'}>
                <div uk-spinner="ratio: 3"></div>
            </div>
        </>
    )
};

const mapStateToProps = (state) => {
    return {
        loading: state.loading,
    }
}

export default connect(mapStateToProps)(Spinner);
