import React, { Fragment } from "react";
import {render} from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from "react-redux";
import App from './App';
import store from "./store";

render((
  <Provider store={store}>
    <BrowserRouter>
      <Fragment>
        <div className="container">
          <h3>TOTO</h3>
          <App  />
        </div>
      </Fragment>
    </BrowserRouter>
  </Provider>
), document.getElementById('root'));