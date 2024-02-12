import React, { Component } from 'react';
import axios from 'axios';
// import Input from '../../components/UI/Input/Input';
// import Button from '../../components/UI/Button/Button';
// import classes from './Login.module.css';
import classes from './Endpoints2.module.css'  ;
import './table.css' ;


class Passesperstation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      stationRef: '',
      dateFrom: '',
      dateTo: '',
      station: [],
      error: '',
      result : [],
      flag: 'false',
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange = event => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  handleSubmit = event => {
    const token = localStorage.getItem('token');
    const { stationRef, dateFrom , dateTo, format } = this.state;; 
    console.log(stationRef, dateFrom, dateTo, format);
    axios({
      method : "get" ,
      url:
        'http://127.0.0.1:9103/interoperability/api/PassesPerStation/' +
        stationRef +
        '/' +
        dateFrom +
        '/' +
        dateTo +
        '?format=' +
        format,
      headers: { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-OBSERVATORY-AUTH': 'token ' + token ,
      },
    })
      .then(response => {
        this.setState({ station: [response.data] });
        this.setState({ result: response.data.PassesList });
        console.log(response.data) ;
      })
      .catch(error => {
        console.log(error.response.data); 
        if(error.response.status !== 200) {
          window.location.href = 'http://localhost:9104/passesperstation';
        } 
        return Promise.reject(error); 
      });
    event.preventDefault();
  }; 


  render() {
    if (this.state.station) {
      return (
        <div className={classes.mainbody}>
          <h2>Passes per station</h2>
          <form onSubmit={this.handleSubmit}>
          <label>Search for passes : </label>
            <input
              type="stationRef"
              name="stationRef"
              placeholder="stationRef"
              value={this.state.stationRef}
              onChange={this.handleChange}
              required
            />
            <input
              type="dateFrom"
              name="dateFrom"
              placeholder="From this date"
              value={this.state.dateFrom}
              onChange={this.handleChange}
              required
            />
            <input
              type="dateTo"
              name="dateTo"
              placeholder="To this date"
              value={this.state.dateTo}
              onChange={this.handleChange}
              required
            />
            <input
              type="format"
              name="format"
              placeholder="Json"
              value={this.state.format}
              onChange={this.handleChange}
              required
            />
            <button type="submit">find</button>
          </form>
          <p>Station Operator is {this.state.station.map(operator => operator.StationOperator)}<br></br>
          The requested timestamp is {this.state.station.map(timestamp => timestamp.RequestTimestamp)} . <br>
          </br>For this period we recorded {this.state.station.map(passes => passes.NumberOfPasses)} passes .<br></br>
          The period is from {this.state.station.map(periodfrom => periodfrom.PeriodFrom)} to {this.state.station.map(periodto => periodto.PeriodTo)} . </p>
          <table>
            <thead>
              <tr>
                <th>PassId</th>
                <th>Timestamp</th>
                <th>Vehicle Ref</th>
                <th>Tag Provider</th>
                <th>Type of pass</th>
                <th>Charge</th>
              </tr>
            </thead>
            <tbody>
              {
                this.state.result.map((stations , index) =>(
                  <tr key={index}>
                    <td>{stations.PassId}</td>
                    <td>{stations.PassTimeStamp}</td>
                    <td>{stations.VehicleID}</td>
                    <td>{stations.TagProvider}</td>
                    <td>{stations.PassType}</td>
                    <td>{stations.PassCharge}</td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        </div>
      );
    } else {
      return (
        <div className={classes.mainbody}>
          <h2>Passes per station</h2>
          <form onSubmit={this.handleSubmit}>
            <label>Search for passes : </label>
            <input
              type="stationRef"
              name="stationRef"
              placeholder="stationRef"
              value={this.state.stationRef}
              onChange={this.handleChange}
              required
            />
            <input
              type="dateFrom"
              name="dateFrom"
              placeholder="From this date"
              value={this.state.dateFrom}
              onChange={this.handleChange}
              required
            />
            <input
              type="dateTo"
              name="dateTo"
              placeholder="To this date"
              value={this.state.dateTo}
              onChange={this.handleChange}
              required
            />
            <input
              type="format"
              name="format"
              placeholder="json"
              value={this.state.format}
              onChange={this.handleChange}
              required
            />
            <button type="submit">find</button>
          </form>
        </div>
      );
    }
  }
}

export default Passesperstation;