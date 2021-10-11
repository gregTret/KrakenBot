import React, { Component } from "react";
import background from "./img/background.png";
import "./App.css";
import { Homepage, Selection, Adjust, Graphpage } from "./components";
import CSSTransitionGroup from "react-transition-group"; // ES6
var CSSTransitionGroup = require("react-transition-group"); // ES5 with npm

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      screen: "home",
    };
  }

  render() {
    return (
      <div
        className="App"
        style={{
          backgroundImage: `url(${background})`,
          backgroundSize: `cover`,
        }}
      >
        <header className="App-header">
          <div class="content">
            {this.state.screen === "home" ? (
              <div>
                <Homepage />
                <button
                  class="krakenButton"
                  onClick={() => this.setState({ screen: "selectionScreen" })}
                >
                  continue
                </button>
              </div>
            ) : this.state.screen === "selectionScreen" ? (
              <div class="content">
                <CSSTransitionGroup
                  transitionName="example"
                  transitionAppear={true}
                  transitionAppearTimeout={500}
                  transitionEnter={true}
                  transitionLeave={false}
                >
                  <Selection />
                  <button
                    class="krakenButton"
                    onClick={() => this.setState({ screen: "home" })}
                  >
                    back
                  </button>
                  <button
                    class="krakenButton"
                    onClick={() => this.setState({ screen: "adjustScreen" })}
                  >
                    continue
                  </button>
                </CSSTransitionGroup>
              </div>
            ) : this.state.screen === "adjustScreen" ? (
              <div>
                <Adjust />
                <button
                  class="krakenButton"
                  onClick={() => this.setState({ screen: "selectionScreen" })}
                >
                  back
                </button>
                <button
                  class="krakenButton"
                  onClick={() => this.setState({ screen: "graphScreen" })}
                >
                  continue
                </button>
              </div>
            ) : this.state.screen === "graphScreen" ? (
              <div>
                <Graphpage />{" "}
                <button
                  class="krakenButton"
                  onClick={() => this.setState({ screen: "home" })}
                >
                  home
                </button>
              </div>
            ) : null}
          </div>
        </header>
      </div>
    );
  }
}

export default App;
