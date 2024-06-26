import React from 'react';
import './style.css';

export const MyForm = () => {
    // Use useState for each input field
    const [webpageLink, setwebpageLink] = React.useState('');
    const [timeInterval, settimeInterval] = React.useState('');
    const [email, setEmail] = React.useState('');
  
    // Event handler for the first input field
    const handleInputChange1 = (event) => {
      // Remove spaces from the input value
      var sanitizedValue = event.target.value.replace(/\s/g, '');
      setwebpageLink(sanitizedValue);
    };
  
    // Event handler for the second input field
    const handleInputChange2 = (event) => {
      settimeInterval(event.target.value);
    };
  
    const handleInputChange3 = (event) => {
      //the email input type will handle the input value. No need to sanitized the value.
      setEmail(event.target.value);
    };
  
    // Submit handler
    const handleSubmit = (event) => {
      //cancel the default submit action of the form, if the page is reloading.
      //somehow fixed the error of console.log not running
      event.preventDefault();
      var regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
      if (!email.match(regex)) {
        alert("Invalid email format.");
        return
      }
      var loading = document.getElementById('loading');
      var display = document.getElementById('display');
      loading.innerHTML = '<span class="loading heroLoading"></span>';
      //'<span class="loading heroLoading"></span>' will automatically 
      //disappear when reload since it is written inside that tag in the DOM not inside the actual html file
      // Send data to Flask backend
      fetch('http://127.0.0.1:5000/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ link: webpageLink, time: timeInterval, clientEmail : email.toLowerCase() }),
      })
        .then(response => response.json())
        .then(result => {
          console.log(result);
          // Handle the response from the Flask backend
          if ((typeof result['value']) === 'number' || result['value'] === "DNS address could not be found. Connection error.") {
            loading.innerHTML = '';
            display.innerHTML = 'ERROR: ' + result['value'] + '<br>The webpage might not exist or is currently down, or do not allow web scraping.<br>Please check the provided link, try again or choose another webpage.'
          } else if (result['value'] === 'invalid url. Must start with https:// or http://' || result['value'] === 'invalid url.') {
            loading.innerHTML = '';
            display.innerHTML = 'ERROR: ' + result['value'];
          } else if((result['value']) === 2) {
            loading.innerHTML = '';
            display.innerHTML = 'ERROR. Can you verify your email. Please check.';
          } else {
            loading.innerHTML = '';
            display.innerHTML = '<iframe id="externalFrame" src="http://127.0.0.1:5500/Website_tracker/Website_Tracker/client/src/viewpage.html" style="width:80%; height: 700px;"></iframe><br><button class="button color" onclick="sendSelected();">Finish</button>';
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

export const Form2 = () => {
    var marg = {
      margin: '20px',
    }
    const [email, setEmail] = React.useState('');
    const handleInputChange = (event) => {
      //the email input type will handle the input value. No need to sanitized the value.
      setEmail(event.target.value);
    };
  
    const handleSubmit = (event) => {
      event.preventDefault();
      console.log(email)
      var display = document.getElementById('display');
      fetch('http://127.0.0.1:5000/unregister', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({clientEmail: email}),
      })
        .then(response => response.json())
        .then(result => {
          if (result['value'] === "Email does not exist in the database. Please check the entered email."){
            display.innerHTML = "<p>Email does not exist in the database. Please check the entered email.</p>";
          } else {
            display.innerHTML = "<p>Unregisted successfully</p>";
          }
        }
      )
      .catch(error => {
        console.error('Error:', error);
      });
    }
    return (
      <form onSubmit={handleSubmit}>
        <label for ="email"><span style={marg}>Want to stop receiving email? Enter your email to unregistser:</span></label>
        <input type = "email" value={email} onChange={handleInputChange} id="email" name="email" required size = "50px"/>
        <input type = "submit" value = "Submit" class = "button color" style={marg}/>
      </form>
    )
  }

//export default {MyForm, Form2};