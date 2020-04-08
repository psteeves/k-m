import React from 'react';
import './App.css';
import SearchBar from './SearchBar';
import * as CoLabAPI from './CoLabAPI';
import Lab from './Lab';

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
                <Lab document={this.state.document}/>
            </div>
        );
    }
}

export default App;
