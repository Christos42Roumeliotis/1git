import React, { Component } from 'react';
import axios from 'axios';
// import Input from '../../components/UI/Input/Input';
// import Button from '../../components/UI/Button/Button';
// import classes from './Login.module.css';
import classes from './Endpoints2.module.css'  ;
import './table.css' ;

class Chargesby extends Component {
  constructor(props) {
    super(props);

    this.state = {
      op_Id: '',
      dateFrom: '',
      dateTo: '',
      station: [],
      result : [],
      error: '',
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
    const { op_Id, dateFrom, dateTo, format } = this.state;
    console.log(op_Id, dateFrom, dateTo, format);
    axios({
      method: 'get',
      url:
        'http://127.0.0.1:9103/interoperability/api/ChargesBy/' +
        op_Id +
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
        this.setState({ result: response.data.PPOList });
        console.log(response.data) ;
      })
      .catch(error => {
        console.log(error.response.data);
        if(error.response.status !== 200) {
          window.location.href = 'http://localhost:9104/chargesby';
        } 
        return Promise.reject(error); 
      });
    event.preventDefault();
  };

  render() {
    if (this.state.station) {
      return (
        <div className={classes.mainbody}>
          <h2>Charges by</h2>
          <form onSubmit={this.handleSubmit}>
          <label>Search : </label>
            <input
              type="op_Id"
              name="op_Id"
              placeholder="op_Id"
              value={this.state.op_Id}
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
          <p>Station Operator is {this.state.station.map(operator => operator.op_ID)}<br></br>
          The requested timestamp is {this.state.station.map(timestamp => timestamp.RequestTimestamp)} . <br></br>
          The period is from {this.state.station.map(periodfrom => periodfrom.PeriodFrom)} to {this.state.station.map(periodto => periodto.PeriodTo)} . </p>
          <table>
            <thead>
              <tr>
                <th>Visiting Operator</th>
                <th>Number of Passes</th>
                <th>Passes Cost</th>
              </tr>
            </thead>
            <tbody>
              {
                this.state.result.map((operators , index) =>(
                  <tr key={index}>
                    <td>{operators.VisitingOperator}</td>
                    <td>{operators.NumberOfPasses}</td>
                    <td>{operators.PassesCost}</td>
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
        <h2>Charges by</h2>
        <form onSubmit={this.handleSubmit}>
          <label>Search : </label>
          <input
            type="op_Id"
            name="op_Id"
            placeholder="op_Id"
            value={this.state.op_Id}
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

export default Chargesby;