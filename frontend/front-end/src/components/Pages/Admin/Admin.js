import React from 'react';
import classes from './Admin.module.css';
import HealthCheck from './AdminEndpoint1' ;
import Button from '../../UI/Button/Button';
import ResetPasses from './AdminEndpoint2';
import ResetVehicles from './AdminEndpoint3';
import ResetStations from './AdminEndpoint3';

const Admin = () => (
  <div className={classes.mainbody}>
    <h2>
      Admin choices:
      </h2>
    <p>
      The administrator of the MetaToll App can do the following :
    </p>
    <Button onClick={HealthCheck}>HealthCheck</Button>
    <Button onClick={ResetPasses}>Reset Passes</Button>
    <Button onClick={ResetStations}>Reset Stations</Button>
    <Button onClick={ResetVehicles}>Reset Vehicles</Button>
  </div>
);

export default Admin;