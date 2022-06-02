import React, { Component } from 'react';
import { connect } from 'react-redux';
import AuthContext from '../../context/AuthContext';

export class Home extends Component {

  static contextType = AuthContext

  render() {
    const { user } = this.context;
    return (
      <div>
        { user && user.email ?
        <h3>Welcome { user.email } !</h3> :
        <h3>Welcome !</h3>
        }
      </div>

      // <div>
      //   { user && user.first_name && user.last_name ?
      //   <h3>Welcome { user.first_name } { user.last_name } !</h3> :
      //   <h3>Welcome !</h3>
      //   }
      // </div>
    );
  }
}

export default connect(
)(Home);