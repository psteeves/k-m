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
            <Card className="result">
                <CardContent className="user-result-left">
                    <Typography variant="h5" gutterBottom >{this.props.user.name}</Typography>
                    <CardMedia>
                        <img className="user-photo" src={im_path} alt="" height="320" width="240"/>
                    </CardMedia>
                    <Button variant="contained" color="primary">Message</Button>
                </CardContent>
                <CardContent className="result-right">
                    <Typography variant="body1" align="left" className="right-pane-title">Relevance Score</Typography>

                    { /* User scores range from 0 to 1 */ }
                    <Typography align="left">{(100 * this.props.user.score).toFixed(0)}%</Typography>

                    <Typography variant="body1" align="left" className="right-pane-title">Details</Typography>
                    <Typography variant="body1" align="left" className="right-pane-item"><i>Email:</i> {this.props.user.email}</Typography>
                    <Typography variant="body1" align="left" className="right-pane-item"><i>Title:</i> {this.props.user.title}</Typography>
                    <Typography variant="body1" align="left" className="right-pane-item"><i>Location:</i> {this.props.user.location}</Typography>
                    <Typography variant="body1" align="left" className="right-pane-title">Internal documents authored</Typography>
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
