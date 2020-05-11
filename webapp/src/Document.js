import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from "@material-ui/core/Button";


class Document extends React.Component {
    render() {
        return (
            <Card className="result">
                <CardContent className="document-result-left">
                    <Typography variant="h5" align="left" gutterBottom >{this.props.document.title}</Typography>
                    <br/>
                    <Typography variant="body1" align="left" gutterBottom>{this.props.document.content.slice(0, 1000) + "..."}</Typography>
                    <br/>
                    <Button variant="contained" color="primary">Open</Button>
                </CardContent>
                <CardContent className="result-right">
                    <Typography variant="body1" align="left" className="right-pane-title">Relevance Score</Typography>
                    {/* User scores range from 0 to 1 */}
                    <Typography variant="body1" align="left">{(100 * this.props.document.score).toFixed(0)}%</Typography>

                    <Typography variant="body1" align="left" className="right-pane-title">Details</Typography>
                    <Typography variant="body1" align="left" className="right-pane-item"><i>Created:</i> {this.props.document.date}</Typography>
                    <Typography variant="body1" align="left" className="right-pane-item"><i>Author:</i> {this.props.document.authors[0]}</Typography>
                </CardContent>
            </Card>
        )
    }
}

export default Document