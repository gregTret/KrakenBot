import React from "react";
import { Link, withRouter } from "react-router-dom";

function Homepage(props) {
    return (
      <div>
        <h3>Kraken Bot</h3>
        <p>a python built api that trades crypto automatically</p>
        <Link class="nav-link" to="/Selection">
          Continue
        </Link>
      </div>
    );
  }
  
export default withRouter(Homepage);