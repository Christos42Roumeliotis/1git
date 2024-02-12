import React from 'react';
// import backgroundPhoto from '../../Assets/images/poggersmobile.jpg';
import classes from './Home.module.css';
import Logo from '../../Logo/Logo';

const Home = () => (
  <div className={classes.mainbody}>
  <h2>
    Welcome to MetaToll Homepage!
  </h2>
  <p>
    We offer:
      <p>
        Great Price : Get the best results easy and quickly.
        </p>
      <p>
        Statistics : Get access to all the statistics you will ever need about the charging records and the passes from your toll stations.
        </p>
      <p>
        Easy to use Services : Our website is designed to be light simple, fast and easy to use.
        </p>
      <p>
        Database : We have a database that contains data for every transaction that happens in our system. Access your data fast and easy!
        </p>
        <Logo />
  </p>
</div>
);
export default Home;
