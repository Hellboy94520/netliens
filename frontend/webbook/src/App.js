import React, { Component } from "react";
import {
  Route,
  Routes
} from "react-router-dom";

import { AuthProvider } from "./content/AuthContext"
import Navbar from "./components/Navbar"
import Home from "./components/home/Home"
import Login from "./components/login/Login";
// import { loadUser } from "./actions/auth";

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
            </Routes>
          </AuthProvider>
      </div>
    );
  }
}

export default App;