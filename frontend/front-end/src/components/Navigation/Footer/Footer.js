import React from 'react';
import FooterItems from '../NavigationItems/FooterItems';
import classes from './Footer.module.css';

const Footer = props => (
  <header className={classes.Footer}>
    <nav className={classes.DesktopOnly}>
      <FooterItems />
    </nav>
  </header>
);
export default Footer;
