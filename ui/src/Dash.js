import React from 'react';
import logo from './logo.svg';
import {
    Alignment,
    Button,
    Classes,
    H5,
    Navbar,
    NavbarDivider,
    NavbarGroup,
    NavbarHeading,
    Switch,
} from "@blueprintjs/core";
import L from 'leaflet';

import './Dash.css';

// https://github.com/Chris502/PureLeafletMap/blob/master/src/Map.jsx

class Dash extends React.Component {
  
  handleClick = () => {this.props.history.push('/apps')};
  render(){
  let position = [ 51.505, -0.09];
  const center = [51.505, -0.09]
  const rectangle = [
    [51.49, -0.08],
    [51.5, -0.06],
  ]
  return (
    <div className="App" >
    </div>
  );
  }
}

export default Dash;
