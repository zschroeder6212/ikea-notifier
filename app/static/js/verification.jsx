import React from 'react';
import ReactDOM from 'react-dom';
import NotificationForm from './components/notification_form.jsx'
import './verification.css';
import './normalize.css';

ReactDOM.render(
      <h1>A verification email has been sent. You must verify tour email before you are notified. Please allow up to 30 minutes for the email to be delivered.</h1>,
      document.getElementById('react-entrypoint')
);