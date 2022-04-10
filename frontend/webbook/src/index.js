// https://reactrouter.com/docs/en/v6/getting-started/tutorial
// https://blog.logrocket.com/migrating-react-router-v6-complete-guide/
import React from 'react';
import ReactDOM from "react-dom";
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import App from "./features/home/App";
import Root from "./Root";

const Loading = () => <p>Loading ...</p>;

ReactDOM.render(
  <React.Suspense fallback={<Loading />}>
    <BrowserRouter>
      <Root />
    </BrowserRouter>
  </React.Suspense>,
  document.getElementById('root')
);
