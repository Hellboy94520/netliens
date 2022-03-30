import React from 'react';
import ReactDOM from 'react-dom';
// import Root from './Root';
import './index.css';
import App from './features/home/App';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.unregister();