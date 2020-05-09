import React from 'react';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import CardMedia from '@material-ui/core/CardMedia';


class User extends React.Component {
    render() {
        const im_path = this.props.user.image_path.replace("/home/psteeves/k-m/data/news-articles/", "");
        return (
            <Card className="user-result">
                <CardContent className="user-result-left">
                    <Typography variant="h5" gutterBottom align="left" className="user-title">{this.props.user.name}</Typography>
                    <CardMedia>
                        <img className="user-photo" src={im_path} alt="" height="320" width="240"/>
                    </CardMedia>
                    <Button variant="outlined" >Message on Slack</Button>
                </CardContent>
                <CardContent>
                    <Typography variant="body1" align="left">Match</Typography>
                    { /* User scores range from 0 to 1, but mostly around 0 */ }
                    <Typography variant="body1" align="left">{(80 * 100 * this.props.user.score).toFixed(0)}%</Typography>
                    <br/>
                    <br/>
                    <Typography variant="body1" align="left">Details</Typography>
                    <Typography variant="body1" align="left">Email: {this.props.user.email}</Typography>
                    <Typography variant="body1" align="left">Title: {this.props.user.title}</Typography>
                    <Typography variant="body1" align="left">Location: {this.props.user.location}</Typography>
                    <Typography variant="body1" align="left">Internal documents authored:</Typography>
                    <ul>
                        {this.props.user.documents.map(doc => (
                            <li key={doc.id}>
                                <Typography align="left">{doc.title}</Typography>
                            </li>
                        ))}
                    </ul>
                </CardContent>
            </Card>
        )
    }
}

export default User;
