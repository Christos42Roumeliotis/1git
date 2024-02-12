import React, { Component } from 'react';
import axios from 'axios';



class ResetPasses extends Component {
    state = {
      systemStatus: ''
    };
  
    axiosStarter = () => {
      const token = localStorage.getItem('token');
      axios({
        method: 'post',
        url: '/admin/resetpasses',
        headers: {
          // 'Content-Type': 'application/x-www-form-urlencoded',
          'XOBSERVATORY-AUTH': token,
        },
      })
        .then(response => {
          this.setState({ systemStatus: JSON.stringify(response.data) });
        })
        .catch(error => {
          console.log(error);
          // console.log(error.response.data);
          // this.setState({ error: error.response.data });
        });
    };
    render() {
      this.axiosStarter();
      if (this.state.systemStatus) {
        return (
          <>
            <h1>System's status:</h1>
            <p>{this.state.systemStatus}</p>
          </>
        );
      } else return <div>Waiting for system's status</div>;
    }
  }
  
  export default ResetPasses;