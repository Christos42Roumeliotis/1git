import React, { Component } from 'react';
import axios from 'axios';
// import Input from '../../components/UI/Input/Input';
// import Button from '../../components/UI/Button/Button';
// import classes from './Login.module.css';
import classes from './Endpoints2.module.css'  ;
import './table.css' ;

class PassesAnalysis extends Component {
  constructor(props) {
    super(props);

    this.state = {
      op1_Id: '',
      op2_Id: '',
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
    const { op1_Id, op2_Id, dateFrom, dateTo, format } = this.state;
    console.log(op1_Id, op2_Id, dateFrom, dateTo, format);
    axios({
      method: 'get',
      url:
        'http://127.0.0.1:9103/interoperability/api/PassesAnalysis/' +
        op1_Id +
        '/' +
        op2_Id +
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
          window.location.href = 'http://localhost:9104/passesanalysis';
        } 
        return Promise.reject(error); 
      });
    event.preventDefault();
  };

  render() {
    if (this.state.station) {
      return (
        <div className={classes.mainbody}>
          <h2>Passes Analysis</h2>
          <form onSubmit={this.handleSubmit}>
            <label>Search : </label>
            <input
              type="op1_Id"
              name="op1_Id"
              placeholder="op1_Id"
              value={this.state.op1_Id}
              onChange={this.handleChange}
              required
            />
            <input
              type="op2_Id"
              name="op2_Id"
              placeholder="op2_Id"
              value={this.state.op2_Id}
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
          <p>Here we have a list of the transit events that took place with Operator2_ID : " {this.state.station.map(operator2 => operator2.op2_ID)} " tag on Operator1 : " 
          {this.state.station.map(operator1 => operator1.op1_ID)} " stations . <br></br>
          The requested timestamp is {this.state.station.map(timestamp => timestamp.RequestTimestamp)} . <br>
          </br>  The period is from {this.state.station.map(periodfrom => periodfrom.PeriodFrom)} to {this.state.station.map(periodto => periodto.PeriodTo)} . <br></br>
          For this period we recorded {this.state.station.map(passes => passes.NumberOfPasses)} passes .</p>
          <table>
            <thead>
              <tr>
                <th>Pass_ID</th>
                <th>Station_ID</th>
                <th>Timestamp</th>
                <th>Vehicle_Id</th>
                <th>Charge</th>
              </tr>
            </thead>
            <tbody>
              {
                this.state.result.map((stations , index) =>(
                  <tr key={index}>
                    <td>{stations.PassId}</td>
                    <td>{stations.StationID}</td>
                    <td>{stations.TimeStamp}</td>
                    <td>{stations.VehicleID}</td>
                    <td>{stations.Charge}</td>
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
        <h2>Passes Analysis</h2>
        <form onSubmit={this.handleSubmit}>
          <label>Search : </label>
          <input
            type="op1_Id"
            name="op1_Id"
            placeholder="op1_Id"
            value={this.state.op1_Id}
            onChange={this.handleChange}
            required
          />
          <input
            type="op2_Id"
            name="op2_Id"
            placeholder="op2_Id"
            value={this.state.op2_Id}
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
      </div>
      );
    }
  }
}

export default PassesAnalysis;