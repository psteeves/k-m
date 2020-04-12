import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';


class User extends React.Component {
    render() {
        return (
            <Card className="user-result">
                <CardContent>
                    <Typography variant="h4" gutterBottom className="user-title">{this.props.user.email}</Typography>
                    <Typography variant="body1" align="left">{this.props.user.email}</Typography>
                </CardContent>
            </Card>
        )

    }
}

export default User;
