import React from 'react'
import {INavalPort,NavalPortsAutoComplete} from '../components/NavalPortsAutoComplete'

export default class Test extends React.Component{
	state = {
		oc1:null,
		oc2:null,
	}
	
	och1 = (item :INavalPort,event) => {
			this.setState({oc1:item})
		}
	
	och2 = (item :INavalPort,event) => {
		this.setState({oc2:item})
	}

	render() {
		
		let c1 = this.state.oc1
		let c2 = this.state.oc2
		return (
			<div style={{'width':'80vw','marginLeft':'10vw'}}>
				<NavalPortsAutoComplete onPortSelected={this.och1} placeHolder={'Search for a port...'}/> 
				<NavalPortsAutoComplete onPortSelected={this.och2}/>
				<br/>
				{JSON.stringify(c1)}
				<br/>
				{JSON.stringify(c2)}

			</div>
			)
	}
}