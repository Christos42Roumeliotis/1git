import React from 'react';
import Toolbar from '../Navigation/Toolbar/Toolbar';
import classes from './Layout.module.css';
import Footer from '../Navigation/Footer/Footer';

const Layout = props => (
  <>
    <Toolbar />
    <main className={classes.Content}>{props.children}</main>
    <Footer />
  </>
);

export default Layout;
