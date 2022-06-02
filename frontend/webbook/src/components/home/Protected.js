import { Component } from "react";
import { connect } from 'react-redux';

export class ProtectedPage extends Component {

  render() {
    return (
      <div>
        <h1>Protected Page</h1>
      </div>
    );
  }
}
export default connect(
)(ProtectedPage);