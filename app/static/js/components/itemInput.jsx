import React from 'react';
import ReactDOM from 'react-dom';
import './itemInput.css';

class ListItems extends React.Component {
      render() {
            return (
                  <React.Fragment>
                        {this.props.vals.map((val, index) =>
                              <div key={index.toString()} className="item" data-value={val}>
                                    {` ${val} `}
                                    <span onClick={() => {this.props.remove(index)}} className="remove-item" title="Remove">×</span>
                              </div>
                        )}
                  </React.Fragment>
            )
      }
}

class ItemInput extends React.Component {

      constructor(props) {
            super(props);
            
            this.state = {
                  items: []
            };
      }

      focusInput(event) {
            if (event.target === event.currentTarget) {
                  event.target.querySelector(".item_input input").focus()
            }
      }

      removeItem = index => {
            this.state.items.splice(index, 1);
            this.setState(this.state);
            this.props.callback(this.state.items);
      }

      addItem = value => {
            this.state.items.push(value);
            this.setState(this.state);
            this.props.callback(this.state.items);
      }

      inputEvent = (event) => {
            let input = event.target;
            let value = event.target.value;
            let keycode = (event.keyCode ? event.keyCode : event.which);
            let parent = input.parentElement;
            if (keycode === 13 || keycode === 188 || keycode === 32 || keycode === 9) {
                  if (value.length > 0) {
                        this.addItem(value)
                        parent.querySelector("input").focus()
                        input.value = "";
                  }
                  event.preventDefault();
            } else if (keycode == 8 && value.length == 0) {
                  this.removeItem(this.state.items.length-1)
            }

      }

      blurEvent = (event) => {
            let input = event.target;
            let value = event.target.value;
            if(value.length > 0) {
                  this.addItem(value);
                  input.value = "";
            }
      }

      changeEvent = (event) => {
            let input = event.target;
            let value = event.target.value;
            let items = value.split(/[, \n]/i);
            if(items.length > 1) {
                  items.forEach(e => {
                        if(e.length > 0)
                              this.addItem(e);
                  });
                  input.value = "";
            }
      }

      render() {
            return (
                  <div className="item_input" id={this.props.id}>
                        <label htmlFor={`${this.props.id}-1`} className="input-label">{this.props.label}</label>
                        <div className="list" onClick={this.focusInput} >
                              <div className="items" onClick={this.focusInput}>
                                    <ListItems remove={this.removeItem} vals={this.state.items} />
                                    <input id={`${this.props.id}-1`} onKeyDown={this.inputEvent} onChange={this.changeEvent} onBlur={this.blurEvent} type="text" />
                              </div>
                        </div>
                  </div>
            )
      }
}

export default ItemInput;