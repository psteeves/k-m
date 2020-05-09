import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class Document extends React.Component {
    render() {
        return (
            <Card className="document-result">
                <CardContent>
                    <Typography variant="h4" gutterBottom className="document-title">{this.props.document.title}</Typography>
                    <Typography variant="body1" align="left">Created: {this.props.document.date}</Typography>
                    <Typography variant="body1" align="left">Author: {this.props.document.authors[0]}</Typography>
                    <Typography variant="body1" align="left">{this.props.document.content}</Typography>
                </CardContent>
            </Card>
        )

    }
}

export default Document