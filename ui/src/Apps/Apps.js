import React from 'react';
import PropTypes from 'prop-types';
import './Apps.css';
import logo from '../logo.svg';
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
    Colors,
    Card,
    Elevation,
    InputGroup,
    Icon
} from "@blueprintjs/core";

export class Apps extends React.Component{
	state = {
		apps:[
			{label:"Route Optimization",icon:'layout'},
			{label:"Weather Updates",icon:'changes'},
			{label:"Previous Routes",icon:'history'},
			{label:"Freet Tracking",icon:'path-search'},	
		],
		search_key: "",
		results: 0
	}

	searchFilter = (item) => {
		if (item['label'].toLowerCase().indexOf(this.state.search_key) >= 0){
			this.results++;
			return true;
		}
		return false;
	}
	handleFilterInput = (event) => {this.setState({search_key:event.target.value,results:0})}
	handleClick = () => {this.props.history.push('/dash')}
	render(){
		const {apps,results} = this.state
	return (
	  <div className="Apps" style={{'background-color':Colors.LIGHT_GRAY5}}>
	    <Navbar>
			<NavbarGroup>
				<NavbarHeading><img src={logo}alt="DSR"/></NavbarHeading>
				<NavbarDivider />
				<Button active={window.location.pathname == "/apps"}className={Classes.MINIMAL} icon="applications" text="Apps" />
			</NavbarGroup>
		</Navbar>
		<Card className="float-menu" elevation={Elevation.THREE}>
			<Card className="app-search" style={{'background-color': Colors.LIGHT_GRAY4}} >
	    		<InputGroup leftIcon="search" onChange={this.handleFilterInput} placeholder="Search in Apps..." />
			</Card>

			<div className="appContainer">
			{ 
				apps.filter(this.searchFilter).map((item) => <div className="appBlock" onClick={this.handleClick}><Icon icon={item.icon} style={{'background-color': Colors.LIGHT_GRAY3,'color': Colors.GRAY1,"padding":"1em","border-radius":"5px"}} iconSize={100} /><br/>{item.label}</div>)
        	}
        	</div>
		</Card>
	  </div>
	);}
}
Apps.propTypes = {};

Apps.defaultProps = {};

export default Apps;
