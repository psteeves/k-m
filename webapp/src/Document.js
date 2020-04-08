import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class Document extends React.Component {
    render() {
        return (
            <Card className="document">
                <CardContent>
                    <Typography variant="h3" gutterBottom className="document-title">{this.props.document.title}</Typography>
                    <Typography variant="body1">{this.props.document.content}</Typography>
                </CardContent>
            </Card>
        )

    }
}

export default Document