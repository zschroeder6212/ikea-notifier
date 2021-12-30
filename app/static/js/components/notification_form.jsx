import React from 'react';
import ReactDOM from 'react-dom';
import ItemInput from './itemInput.jsx'
import './notification_form.css';

class NotificationForm extends React.Component {

    updateArticles = (articles) => {
        console.log(articles);
    }

    render() {
        return(
            <div id="form-box">
                <ItemInput id="articles" callback={this.updateArticles} />
                <input type="text" id="zip_code" />
                <input type="email" id="email_address"/>
                <input type="submit" id="submit_button" value="SUBMIT" />
            </div>
        )
    }
}

export default NotificationForm