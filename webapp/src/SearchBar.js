import React from "react";
import Button from '@material-ui/core/Button';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import DescriptionIcon from '@material-ui/icons/Description';
import AssessmentIcon from '@material-ui/icons/Assessment';


class SearchBar extends React.Component {
  render() {
    return (
        <div className="search-bar">
            <Button className="search-button">
              content lab
              <AssessmentIcon className="search-icon"/>
          </Button>
          <Button className="search-button">
              search documents
              <DescriptionIcon className="search-icon"/>
          </Button>
          <Button className="search-button">
              search experts
              <AccountBoxIcon className="search-icon"/>
          </Button>
        </div>
    )
  }
}

export default SearchBar;
