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

const Loading = () => <p>Loading ...</p>;

ReactDOM.render(
  <React.Suspense fallback={<Loading />}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.Suspense>,
  document.getElementById('root')
);
