import React from 'react';
import User from './User';
import Typography from '@material-ui/core/Typography';
import { searchUsers } from "./CoLabAPI";


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
        return (
            <div>
                <Typography variant="h3">Most relevant internal experts</Typography>
                <div className="user-results-list">
                {this.state.users.map(user => <User user={user}/>)}
                </div>
            </div>
        )
    }
}

export default UserResults;
