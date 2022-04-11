import React, { Fragment } from 'react';
import { Provider as AlertProvider } from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'

// import { HashRouter as BrowserRouter, Router, Route, Switch, Redirect } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../store';

import { Home } from './home/Home'
import Alerts from './common/Alerts';

const alertOptions = {
  timeout: 3000,
  position: 'top center'
}

export default function App() {
  return (
    <Provider store={store}>
      <AlertProvider template={AlertTemplate} {...alertOptions}>
        <Fragment>
          <Alerts/>
          <Home/>
        </Fragment>
      {/* <BrowserRouter>
        <Router>
          <Route exact path='/' component={Home}/>
        </Router>
      </BrowserRouter> */}
      </AlertProvider>
    </Provider>

  )
}
