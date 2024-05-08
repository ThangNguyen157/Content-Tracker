import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import {MyForm, Form2} from './App';

import reportWebVitals from './reportWebVitals';

function sendSelected(){

  var frame = document.getElementById("externalFrame");
  
  console.log(frame.contentWindow.ids);
  if(Object.keys(frame.contentWindow.ids).length === 0) {
    alert('Please select something before submiting');
    return
  }

  fetch('http://127.0.0.1:5000/tags', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ids: frame.contentWindow.ids}),
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // Handle the response from the Flask backend
    })
    .catch(error => {
      console.error('Error:', error);
    });
    window.location.reload();
}

//ReactDOM.render(<MyForm/>, document.querySelector('#form'));
//ReactDOM.render(<Form2/>, document.querySelector('#unregister'));

const root1 = ReactDOM.createRoot(document.getElementById('form'));
root1.render(
  <React.StrictMode>
    <MyForm />
  </React.StrictMode>
);

const root2 = ReactDOM.createRoot(document.getElementById('unregister'));
root2.render(
  <React.StrictMode>
    <Form2 />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

//import React from 'react';
//import ReactDOM from 'react-dom';
//import './style.css'

/*class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      webpageLink: '',
      timeInterval: '',
      email: '',
    };
    this.handleInputChange1 = this.handleInputChange1.bind(this);
    this.handleInputChange2 = this.handleInputChange2.bind(this);
    this.handleInputChange3 = this.handleInputChange3.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleInputChange1 = (event) => {
    this.setState({webpageLink : event.target.value})
  };

  // Event handler for the second input field
  handleInputChange2 = (event) => {
    this.setState({timeInterval : event.target.value})
  };

  handleInputChange3 = (event) => {
    this.setState({email : event.target.value})
  };

  handleSubmit = () => {
    // Send data to Flask backend
    fetch('http://127.0.0.1:5000/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'link': this.state.webpageLink, 'time': this.state.timeInterval, 'clientEmail' : this.state.email }),
    })
      .then(res => {
        // Check if the response status is OK
        if (!res.ok) {
          logs()
        } else {
          logs()
        }
        return res.json();
      })
      .then(result => {
        logs()
        // Handle the response from the Flask backend
        if ((typeof result['value']) == 'number') {
          generateError(result['value'])
          console.log("errorrrrr")
        } else {
          console.log("success1");
          var tag = document.getElementById("response");
          tag.innerHTML = result['value'].toString()
          console.log("success2")
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  render() {
    console.log("22222")
    return (
    <>
      <form onSubmit={this.handleSubmit}>
         <label for ="webpageLink"><p class = "heroSubText color">Link to the webpage:</p></label>
          <input type="text" value ={this.state.webpageLink} onChange={this.handleInputChange1} name="webpageLink" id = "webpageLink" size = "50px" maxlength="9999" required/>
          <label for="timeInterval"><p class = "inputText color">Time interval (minutes):</p><p  class = "inputSubText color">The webpage will be check after every this amount of time. Minimum is 10 mins to avoid any bad consequences due to web scraping.</p></label>
          <input type="number" value={this.state.timeInterval} onChange={this.handleInputChange2} id="timeInterval" name="timeInterval" min="10" max = "999999"step="1" placeholder="10-999999" required/>
          <label for ="email"><p class = "inputText color">Email:</p></label>
          <input type = "email" value={this.state.email} onChange={this.handleInputChange3} id="email" name="email" required size = "50px"/><br/>
          <input type = "submit" value = "GO!" class = "button color"/>
      </form>
    </>
    );
  }

}*/