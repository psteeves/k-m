import React from 'react';
import './App.css';
import SearchBar from './SearchBar';
import * as CoLabAPI from './CoLabAPI';
import Lab from './Lab';
import DocumentResults from './DocumentResults';
import { Route } from 'react-router-dom';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {document: {title: '', content: '', representation: [], topics: {}}}
    }

    componentDidMount() {
        CoLabAPI.getDemoDocument().then(document => {
            this.setState({ document })
        })
    }

    render() {
        return (
            <div className="App">
                <header>
                    /<h1 className="company-name">CoLab</h1>
                </header>
                <SearchBar/>
                <Route exact path="/" render={() => (
                    <Lab document={this.state.document}/>
                )}
                />
                <Route path="/documents" render={() => (
                    <DocumentResults document={this.state.document}/>
                )}
                />
                <Route path="/users" render={() => (
                    "Not implemented yet!"
                )}
                />
            </div>
        );
    }
}

export default App;
