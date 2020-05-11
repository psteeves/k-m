import React from 'react';
import User from './User';
import Typography from '@material-ui/core/Typography';
import { searchUsers } from "./CoLabAPI";
import Progress from "./Progress";


class UserResults extends React.Component {
    constructor(props) {
        super(props);
        this.state = {users: []}
    }
    componentDidMount() {
        searchUsers(this.props.document.content)
            .then(users => {
                this.setState({ users })
            })
    }

    render() {
        const results = this.state.users.length === 0 ?  <Progress/> : this.state.users.map(user => <User user={user}/>)
        return (
            <div>
                <Typography variant="h3">Relevant internal experts</Typography>
                <div className="results-list">
                    {results}
                </div>
            </div>
        )
    }
}

export default UserResults;
