
// import React, { Component, Fragment } from "react";
// import ReactDOM from "react-dom";
// import {
//   HashRouter as Router,
//   Route,
//   Routes,
// } from "react-router-dom";
// import { AuthProvider } from "./context/AuthContext";

// import { Provider as AlertProvider } from "react-alert";
// import AlertTemplate from "react-alert-template-basic";

// import axiosInstance from "./axiosApi"
// import Home from "./components/home/Home";
// import Login from "./components/login/Login";
// import Alerts from "./components/layout/Alerts";

// import { Provider } from "react-redux";
// import store from "./store";
// // import { loadUser } from "./actions/auth";

// // Alert Options
// const alertOptions = {
//   timeout: 3000,
//   position: "top center",
// };

// class App extends Component {
//   componentDidMount() {
//     this.handleLogout = this.handleLogout.bind(this);
//   }

//   async handleLogout() {
//     try {
//         const response = await axiosInstance.post('/blacklist/', {
//             "refresh_token": localStorage.getItem("refresh_token")
//         });
//         localStorage.removeItem('access_token');
//         localStorage.removeItem('refresh_token');
//         axiosInstance.defaults.headers['Authorization'] = null;
//         return response;
//     }
//     catch (e) {
//         console.log(e);
//     }
// };

//   render() {
//     return (
//       <Provider store={store}>
//         <AlertProvider template={AlertTemplate} {...alertOptions}>
//           <Router>
//             <AuthProvider>
//               <Fragment>
//                 {/* <Header /> */}
//                 <Alerts />
//                 <div className="container">
//                   <Routes>
//                     <Route path="home/" element={<Home />}></Route>
//                     <Route exact path="login/" element={<Login />}></Route>
//                   </Routes>
//                 </div>
//               </Fragment>
//             </AuthProvider>
//           </Router>
//         </AlertProvider>
//       </Provider>
//     );
//   }
// }

// ReactDOM.render(<App />, document.getElementById("root"));


import React, { Component } from "react";
import ReactDOM from "react-dom";
import {
  Route,
  Routes,
} from "react-router-dom";

import axiosInstance from "./axiosApi"
import Home from "./components/home/Home";
import Login from "./components/login/Login";
// import { loadUser } from "./actions/auth";

class App extends Component {
  componentDidMount() {
    this.handleLogout = this.handleLogout.bind(this);
  }

  async handleLogout() {
    try {
        const response = await axiosInstance.post('/blacklist/', {
            "refresh_token": localStorage.getItem("refresh_token")
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axiosInstance.defaults.headers['Authorization'] = null;
        return response;
    }
    catch (e) {
        console.log(e);
    }
};

  render() {
    return (
      <div className="container">
        <Routes>
          {/* <Route path="/home/" element={<Home />}></Route> */}
          <Route exact path="/login/" element={<Login />}></Route>
        </Routes>
      </div>
    );
  }
}

export default App;