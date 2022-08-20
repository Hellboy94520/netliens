import React, { Component } from "react";
import {
  Route,
  Routes
} from "react-router-dom";

import { AuthProvider } from "./context/AuthContext"
import Navbar from "./components/Navbar"
import Home from "./components/home/Home"
import Login from "./components/login/Login";
import ProtectedPage from "./components/home/Protected";
import CategoryPage from "./components/home/Category";

import PrivateRoute from "./utils/AuthRoute";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      logged_in: localStorage.getItem('token') ? true : false,
      username: '',
    }
  }

  render() {
    return (
      <div className="container">
          <AuthProvider>
            <Navbar/>
            <Routes>
              <Route path="/" element={<Home />}/>
              <Route exact path="/login/" element={<Login />}/>
              <Route path="/category/" element={<CategoryPage />}/>
              <Route element={
                <PrivateRoute>
                  <ProtectedPage />
                </PrivateRoute>
              } path="/protected" exact />
            </Routes>
          </AuthProvider>
      </div>
    );
  }
}

export default App;