import { Link } from "react-router-dom";
import React, { Component } from 'react';
import PropTypes from 'prop-types';

export class App extends Component {
  static propTypes = {
  };

  render() {
    return (
      <div>
        <h1>Bookkeeper</h1>
        <nav
          style={{
            borderBottom: "solid 1px",
            paddingBottom: "1rem",
          }}
        >
          <Link to="/invoices">Invoices</Link> |{" "}
          <Link to="/expenses">Expenses</Link>
        </nav>
      </div>
    );
  }
}
export default App()();
