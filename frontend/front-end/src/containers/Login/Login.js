import React, { Component } from 'react';
import qs from 'qs';
// const qs = require('qs');
import Input from '../../components/UI/Input/Input';
import Button from '../../components/UI/Button/Button';
import classes from './Login.module.css';
import axios from 'axios';

class Login extends Component {
  state = {
    controls: {
      username: {
        elementType: 'input',
        elementConfig: {
          type: 'text',
          placeholder: 'Your username',
        },
        value: '',
        validation: {
          required: true,
          minLength: 5,
        },
        valid: false,
        touched: false,
      },
      password: {
        elementType: 'input',
        elementConfig: {
          type: 'password',
          placeholder: 'Your password',
        },
        value: '',
        validation: {
          required: true,
          minLength: 5,
        },
        valid: false,
        touched: false,
      },
    },
    error: [],
  };

  checkValidity(value, rules) {
    let isValid = true;
    if (!rules) {
      return true;
    }

    if (rules.required) {
      isValid = value.trim() !== '' && isValid;
    }

    if (rules.minLength) {
      isValid = value.length >= rules.minLength && isValid;
    }

    if (rules.maxLength) {
      isValid = value.length <= rules.maxLength && isValid;
    }

    if (rules.isEmail) {
      const pattern = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/;
      isValid = pattern.test(value) && isValid;
    }

    if (rules.isNumeric) {
      const pattern = /^\d+$/;
      isValid = pattern.test(value) && isValid;
    }

    return isValid;
  }

  inputChangedHandler = (event, controlName) => {
    const updatedControls = {
      ...this.state.controls,
      [controlName]: {
        ...this.state.controls[controlName],
        value: event.target.value,
        valid: this.checkValidity(
          event.target.value,
          this.state.controls[controlName].validation
        ),
        touched: true,
      },
    };
    this.setState({ controls: updatedControls });
  };

  submitHandler = event => {
    event.preventDefault();
    console.log('props', this.props);
    console.log(this.state);
    const username = this.state.controls.username.value;
    const password = this.state.controls.password.value;

    const data = qs.stringify({
      username: username,
      password: password,
    });
    console.log('Credentials: ', username, password);

    axios({
      method: 'post',
      url: 'http://127.0.0.1:9103/interoperability/api/login/',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      data: data,
    })
      .then(response => {
        console.log(response);
        let dataa = JSON.stringify(response.data);
        let token = dataa.split(':"')[1];
        token = token.substring(0, token.length - 2);
        console.log(token);
        localStorage.setItem('token', token);
        window.location.href = 'http://localhost:9104/';
        // window.location.reload();
        console.log('i have to push');
        // this.props.history.push('/');
        console.log('i pushed');

        // this.props.history.push('/');
        //to get token localStorage.getItem('itemName')
      })
      .catch(error => {
        console.log(error.response.data);
        //this.setState({ error: error.response.data });
        if(error.response.status !== 200) {
          window.location.href = 'http://localhost:9104/login';
        } 
        return Promise.reject(error); 
    });
  };
  render() {
    const formElementsArray = [];
    for (let key in this.state.controls) {
      formElementsArray.push({
        id: key,
        config: this.state.controls[key],
      });
    }
    const form = formElementsArray.map(formElement => (
      <Input
        key={formElement.id}
        elementType={formElement.config.elementType}
        elementConfig={formElement.config.elementConfig}
        value={formElement.config.value}
        invalid={!formElement.config.valid}
        shouldValidate={formElement.config.validation}
        touched={formElement.config.touched}
        changed={event => this.inputChangedHandler(event, formElement.id)}
      />
    ));
    return (
      <div className={classes.Auth}>
        <form>
          {form}
          <Button btnType="Sucess" clicked={this.submitHandler}>
            Submit
          </Button>
        </form>
        <p className={classes.ErrorStyle}>{this.state.error}</p>
      </div>
    );
  }
}

export default Login;
