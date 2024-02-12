import React from 'react';
import classes from './FooterItems.module.css';

const FooterItems = () => (
  <ul className={classes.FooterItems}>
    {/* <NavigationItem link="/contact">Contact</NavigationItem> */}

    <a href="https://github.com/ntua/TL21-28" target="_blank" rel="noreferrer">
      Github
    </a>
  </ul>
);

export default FooterItems;
