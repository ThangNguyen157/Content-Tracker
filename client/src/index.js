class MyForm extends React.Component {
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
      body: JSON.stringify({Link: this.state.webpageLink, time: this.state.timeInterval, clientEmail : this.state.email }),
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        // Handle the response from the Flask backend
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  render() {
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

}

ReactDOM.render(<MyForm/>, document.querySelector('#form'));
/*
const MyForm = () => {
  // Use useState for each input field
  const [webpageLink, setwebpageLink] = useState('');
  const [timeInterval, settimeInterval] = useState('');
  const [email, setEmail] = useState('');

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
  const handleSubmit = () => {
    // Send data to Flask backend
    fetch('api/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ Link: webpageLink, time: timeInterval, clientEmail : email }),
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        // Handle the response from the Flask backend
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  return (
    <span>
      <form>
         <label for ="webpageLink"><p class = "heroSubText color">Link to the webpage:</p></label>
          <input type="text" value ={webpageLink} onChange={handleInputChange1} name="webpageLink" id = "webpageLink" size = "50px" maxlength="9999" required/>
          <label for="timeInterval"><p class = "inputText color">Time interval (minutes):</p><p  class = "heroSubText color" style = "font-size: 15px;">The webpage will be check after every this amount of time. Minimum is 10 mins to avoid any bad consequences due to web scraping.</p></label>
          <input type="number" value={timInterval} onChange={handleInputChange2} id="timeInterval" name="timeInterval" min="10" max = "999999"step="1" placeholder="10-999999" required/>
          <label for ="email"><p class = "inputText color">Email:</p></label>
          <input type = "email" value={email} onChange={handleInputChange3} id="email" name="email" required size = "50px"/><br/>
          <input type = "submit" value = "GO!" class = "button color" onClick={handleSubmit}/>
      </form>
    </span>
  );
};

const domContainer = document.querySelector('#root');
const root = ReactDOM.createRoot(domContainer);
root.render(e(LikeButton));

export default MyForm;
*/