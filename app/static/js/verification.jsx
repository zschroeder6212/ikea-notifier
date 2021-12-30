import React from 'react';
import ReactDOM from 'react-dom';
import NotificationForm from './components/notification_form.jsx'
import './verification.css';
import './normalize.css';

ReactDOM.render(
    <div id="message-box">
        <h2>Success!</h2>
        <div id="inner-box">
            <span class="notification">A verification email has been sent. You must verify your email before you are notified. Please allow up to 30 minutes for the email to be delivered.</span>
        </div>
    </div>,
    document.getElementById('react-entrypoint')
);