import React from 'react';
import classes from './About.module.css';

const About = () => (
  <div className={classes.mainbody}>
    <h2>
      About us:
      </h2>
    <p>
      This website was created for the semester project of the course: <br />
      "Software Engineering" of NTUA ECE School.
      <br /> Course is currently in the 7th semester.
      <br /> <br />
      Our team consists of: <br /> Konstantinos Kefalas , 
      Christos Roumeliotis , Spyridon Gourgoutas . 
      <br /> The github repository for this whole project is in the footer of
      the page.
    </p>
  </div>
);

export default About;