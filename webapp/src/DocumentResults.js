import React from 'react';
import Document from './Document';
import Typography from '@material-ui/core/Typography';
import { searchDocuments } from "./CoLabAPI";
import Progress from "./Progress";


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
        const results = this.state.documents.length === 0 ?  <Progress/> : this.state.documents.map(doc => <Document document={doc}/>);
        return (
            <div>
                <Typography variant="h3">Relevant internal documents</Typography>
                <div className="results-list">
                {results}
                </div>
            </div>
        )
    }
}

export default DocumentResults;
