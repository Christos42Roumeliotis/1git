import React from 'react';
import classes from './NavigationItem.module.css';
import { NavLink } from 'react-router-dom';

const NavigationItem = props => {
  if (props.auth) return null;
  else {
    return (
      <ul className={classes.NavigationItem}>
        <NavLink to={props.link} exact activeClassName={classes.active}>
          {props.children}
        </NavLink>
      </ul>
    );
  }
};

export default NavigationItem;
