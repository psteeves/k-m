import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class Document extends React.Component {
    render() {
        return (
            <Card className="document-result">
                <CardContent className="document-result-left">
                    <Typography variant="h4" align="left" gutterBottom >{this.props.document.title}</Typography>
                    <br/>
                    <Typography variant="body1" align="left">{this.props.document.content}</Typography>
                </CardContent>
                <CardContent>
                    <Typography variant="body1" align="left">Match</Typography>
                    {/* User scores range from 0 to 1 */}
                    <Typography variant="body1" align="left">{(100 * (1 - this.props.document.score)).toFixed(0)}%</Typography>
                    <br/>
                    <br/>
                    <Typography variant="body1" align="left">Details</Typography>
                    <Typography variant="body1" align="left">Created: {this.props.document.date}</Typography>
                    <Typography variant="body1" align="left">Author: {this.props.document.authors[0]}</Typography>
                </CardContent>
            </Card>
        )

    }
}

export default Document