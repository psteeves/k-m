import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class User extends React.Component {
    render() {
        return (
            <Card className="user-result">
                <CardContent>
                    <Typography variant="h5" gutterBottom className="user-title">{this.props.user.name}</Typography>
                    <Typography variant="body1" align="left">Email: {this.props.user.email}</Typography>
                    <Typography variant="body1" align="left">Title: {this.props.user.title}</Typography>
                    <Typography variant="body1" align="left">Location: {this.props.user.location}</Typography>
                    <Typography variant="body1" align="left">Authored:</Typography>
                    <ul>
                        {this.props.user.documents.map(doc => <li>
                            <Typography align="left">{doc.title}</Typography>
                        </li>)}
                    </ul>
                </CardContent>
            </Card>
        )
    }
}

export default User;
