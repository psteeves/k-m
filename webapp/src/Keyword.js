import React from 'react';
import Typography from '@material-ui/core/Typography';


class Keyword extends React.Component {
    render() {
        return (
                <Typography>{this.props.keyword}</Typography>
        )
    }
}

export default Keyword;