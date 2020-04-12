import React from 'react';
import Document from './Document';
import Typography from '@material-ui/core/Typography';
import { searchDocuments } from "./CoLabAPI";


class DocumentResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {documents: []}
    }
    componentDidMount() {
        searchDocuments(this.props.document.content)
            .then(documents => {
                this.setState({ documents })
            })
    }

    render() {
        return (
            <div>
                <Typography variant="h3">Most similar internal documents</Typography>
                <div className="doc-results-list">
                {this.state.documents.map(doc => <Document document={doc}/>)}
                </div>
            </div>
        )
    }
}

export default DocumentResults;
