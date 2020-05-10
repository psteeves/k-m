import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import LabAnalysis from './LabAnalysis';


class Lab extends React.Component {
     createContentDisplay(content) {
         return content.slice(0, 2000) + "..."
    }

    render() {
        return (
            <div className="doc-lab">
                <Card className="doc-content">
                    <CardContent>
                        <Typography variant="h3" gutterBottom className="content-title">What You're Reading</Typography>
                        <Typography variant="body1">{this.createContentDisplay(this.props.document.content)}</Typography>
                    </CardContent>
                </Card>
                <Card className="doc-analysis">
                    <CardContent>
                        <Typography variant="h3" gutterBottom className="analysis-title">Content Analysis</Typography>
                        <LabAnalysis document={this.props.document} />
                    </CardContent>
                </Card>
            </div>
        )
    }
}

export default Lab;