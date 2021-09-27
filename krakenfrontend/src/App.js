import background from './img/background.png';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { Homepage, Selection, Adjust, Graphpage } from './components';

function App() {
  return (
    <div className="App" style={{ backgroundImage: `url(${background})`, backgroundSize: `cover`}}>
       <Router>
        <header className="App-header">
          <Homepage />
          <Switch>
            <Route path="/Selection" exact component={() => <Selection />} />
          </Switch>
          <Adjust />
          <Graphpage />
        </header>
      </Router>
    </div>
  );
}

export default App;
