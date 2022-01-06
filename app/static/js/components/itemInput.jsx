import React from 'react';
import ReactDOM from 'react-dom';
import './itemInput.css';

class ListItems extends React.Component {
      render() {
            return (
                  <React.Fragment>
                        {this.props.vals.map((val, index) =>
                              <div key={index.toString()} className="item" data-value={val}>
                                    <span onClick={() => {this.props.edit(index)}} class="item-value">{` ${val} `}</span>
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

            this.itemInput = React.createRef();
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

      editItem = index => {
            this.itemInput.current.value = this.state.items[index];
            this.removeItem(index);
            this.itemInput.current.focus();
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
                        <div className="list" onClick={this.focusInput} >
                              <div className="items" onClick={this.focusInput}>
                                    <ListItems edit={this.editItem} remove={this.removeItem} vals={this.state.items} />
                                    <input ref={this.itemInput} onKeyDown={this.inputEvent} onChange={this.changeEvent} onBlur={this.blurEvent} type="text" />
                              </div>
                        </div>
                  </div>
            )
      }
}

export default ItemInput;