import React from 'react';
import ReactDOM from 'react-dom';
import ItemInput from './itemInput.jsx'
import './notification_form.css';

class NotificationForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'countries': [],
            'articles': []
        };
    }

    updateArticles = (articles) => {
        this.state.articles = articles;
        this.setState(this.state);
    }

    getCountries = () => {
        fetch(`/api/get_countries`)
        .then(response => response.json())
        .then(json => {
            this.state.countries = json;
            console.log(this.state.countries)
            this.setState(this.state);
        });
    }

    componentDidMount() {
        this.getCountries();
    }

    submitForm = () => {
        let email = document.getElementById('email_address').value
        let zip_code = document.getElementById('zip_code').value
        let country = document.getElementById('country_code').value

        var data = {
            'email': email,
            'country_code': country,
            'zip_code': zip_code,
            'items': this.state.articles
        };

        console.log(data);

        fetch('/api/notifier/add_notification', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(res => res.json())
        .then(data => {
            console.log(data);
            if(data.code !== 'OK')
            {
                alert(`Error: ${data.code}`)
            }else {
                window.location.href = (`/verification`);
            }
        });
    }

    render() {
        return(
            <div id="form-box">
                <div id="title">IKEA Notifier</div>
                <div id="inner-box">
                    <label for="email_address">Email Address:</label>
                    <input class="form" type="email" id="email_address"/>

                    <label for="zip_code">Zip Code:</label>
                    <input class="form" type="text" id="zip_code" />

                    <label for="country_code">Country:</label>
                    <select class="form" name="country" id="country_code">
                        {this.state.countries.map((country, index) =>
                            <option value={country.code} key={index}>{country.name}</option>
                        )}
                    </select>
                    
                    <label for="articles">Article Number(s):</label>
                    <ItemInput id="articles" callback={this.updateArticles} />

                    <input onClick={this.submitForm} class="form" type="submit" id="submit_button" value="SUBMIT" />
                </div>
                
            </div>
        )
    }
}

export default NotificationForm