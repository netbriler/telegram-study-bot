import { connect } from 'react-redux';
import React from 'react';

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
