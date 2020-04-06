import React from 'react';
import './App.css';
import SearchBar from './SearchBar';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {document: {title: '', content: ''}}
    }

    componentDidMount() {

    }

    render() {
        return (
            <div className="App">
                <header>
                    /<h1 className="company-name">CoLab</h1>
                </header>
                <SearchBar/>
            </div>
        );
    }
}

export default App;
