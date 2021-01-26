import React from 'react'
import { Suggest } from "@blueprintjs/select";
import { MenuItem,Spinner } from "@blueprintjs/core";
import axios from 'axios';
import constants from '../constants.js'

export interface INavalPort {
    world_port_index: number;
    main_port_name: string;
    wpi_country: string;
    region: string;
    lat: number;
    lon: number;
}

export class NavalPortsAutoComplete extends React.Component{
	state = {
		items:[],
		loading: false,
	}
	autocomplete = (query,event) => {
		if(event){
			this.setState({loading:true})
			axios.get(constants()['API_URL']+"/ports/naval?q="+query).then(
				(response) => {
					this.setState({items:response.data.results,loading:false})
				}
				);
		}
	}

	render = () => {
		let itemRender = (item, {handleClick, modifiers, query }) => {
			return (
		        <MenuItem
		        	style={{"textTransform":"capitalize"}}
		            label={item.wpi_country + ", " + item.world_port_index}
		            key={item.world_port_index}
		            onClick={handleClick}
		            text={item.main_port_name}

		        />
		    );
		};
		
		let itemSelect = (item :INavalPort) => {
			if(this.props.onPortSelected){
				this.props.onPortSelected(item)
			}
		};

		let inputRender = (item) => item.main_port_name
		return (
			<div style={{'position':'relative'}}>
				<div style={{'position':'absolute','zIndex':'10','top':5,'right':5}}>
					{ this.state.loading ? <Spinner size={Spinner.SIZE_SMALL} /> : null }
				</div>
				<Suggest 
					items={this.state.items} 
					onQueryChange={this.autocomplete} 
					popoverProps={{minimal:true,fill:true}} 
					itemRenderer={itemRender}
					onItemSelect={itemSelect}
					inputValueRenderer={inputRender}
					inputProps={{placeholder: this.props.placeHolder}} 
					noResults={<MenuItem disabled={true} text={"No Results"}/>}
					
					/>
			</div>
			);
	}
}