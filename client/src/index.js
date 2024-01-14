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

function generateError() {
  ReactDOM.render(<ErrorMessage/>, document.querySelector('#response'));
}

const MyForm = () => {
  // Use useState for each input field
  const [webpageLink, setwebpageLink] = React.useState('');
  const [timeInterval, settimeInterval] = React.useState('');
  const [email, setEmail] = React.useState('');

  // Event handler for the first input field
  const handleInputChange1 = (event) => {
    setwebpageLink(event.target.value);
  };

  // Event handler for the second input field
  const handleInputChange2 = (event) => {
    settimeInterval(event.target.value);
  };

  const handleInputChange3 = (event) => {
    setEmail(event.target.value);
  };

  // Submit handler
  const handleSubmit = (event) => {
    //cancel the default submit action of the form, if the page is reloading.
    //somehow fixed the error of console.log not running
    event.preventDefault();

    var loading = document.getElementById("loading");
    loading.innerHTML = '<span class="loading heroLoading"></span>';
    //'<span class="loading heroLoading"></span>' will automatically 
    //disappear when reload since it is written inside that tag in the DOM not inside the actual html file
    // Send data to Flask backend
    fetch('http://127.0.0.1:5000/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ link: webpageLink, time: timeInterval, clientEmail : email }),
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        // Handle the response from the Flask backend
        if ((typeof result['value']) === 'number' || result['value'] === 'DNS address could not be found') {
          frame.innerHTML = 'error: ' + result['value'] + '<br>The webpage might not exist or is currently down, or do not allow web scraping.<br>Please check the provided link, try again or choose another webpage.'
        } else {
          loading.innerHTML = '';
          frame.innerHTML = '<iframe id="externalFrame" src="viewpage.html" style="width:80%; height: 700px;"></iframe><br><br><button onclick="sendSelected();">Finish</button>';
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
         <label for ="webpageLink"><p class = "heroSubText color">Link to the webpage:</p></label>
          <input type="text" value ={webpageLink} onChange={handleInputChange1} name="webpageLink" id = "webpageLink" size = "50px" maxlength="9999" required/>
          <label for="timeInterval"><p class = "inputText color">Time interval (minutes):</p><p  class = "inputSubText color">The webpage will be check after every this amount of time. Minimum is 10 mins to avoid any bad consequences due to web scraping.</p></label>
          <input type="number" value={timeInterval} onChange={handleInputChange2} id="timeInterval" name="timeInterval" min="10" max = "999999"step="1" placeholder="10-999999" required/>
          <label for ="email"><p class = "inputText color">Email:</p></label>
          <input type = "email" value={email} onChange={handleInputChange3} id="email" name="email" required size = "50px"/><br/>
          <input type = "submit" value = "GO!" class = "button color"/>
      </form>
    </>
  );
};

ReactDOM.render(<MyForm/>, document.querySelector('#form'));



function sendSelected(){

  var frame = document.getElementById("externalFrame");
  console.log(11111111111111111);
  console.log(frame.contentWindow.ids);


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
}

export default MyForm