import React from 'react';
import classes from './Endpoints.module.css';


const Endpoints = () => {
  return (
    <div className={classes.mainbody}>
      <h2>This is the endpoints page</h2>
      <p>
        From here every stakeholder can check :
        <br /> <br />
        <li> Their passes per station: </li>
        <a href="/passesperstation">Passes per station</a>
        <li>
          {' '}
          A passes analysis of the transit events that took place with op2_ID
          tag on op1_ID stations :{' '}
        </li>
        <a href="/passesanalysis">Passes Analysis</a>
        <li>
          {' '}
          The number of the transit events that took place with op2_ID tag on
          op1_ID stations , as well as the the amount of money op1 owes to op2
          for the given period:{' '}
        </li>
        <a href="/passescost">Passes Cost</a>
        <li>
          {' '}
          The number of the transit events that took place on op_ID stations ,
          as well as the the amount of money every other operator owes to this
          one for the given period:{' '}
        </li>
        <a href="/chargesby">Charges by</a>
      </p>
    </div>
  );
};

export default Endpoints;