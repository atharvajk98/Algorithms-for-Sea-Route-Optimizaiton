import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import "normalize.css";
import "@blueprintjs/core/lib/css/blueprint.css";
import "@blueprintjs/icons/lib/css/blueprint-icons.css";
import Home from './Home/Home';
import Apps from './Apps/Apps';
import Dash from './Dash'
import Test from './test/test';

import * as serviceWorker from './serviceWorker';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom'

const routing = (
  <Router>
    <div>
      <Route exact path="/" component={Home} />
      <Route exact path="/static/index.html" component={Home} />
      <Route path="/apps" component={Apps} />
      <Route path="/dash" component={Dash} />
      <Route path="/test" component={Test} />
    </div>
  </Router>
)
ReactDOM.render(
  routing,document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
