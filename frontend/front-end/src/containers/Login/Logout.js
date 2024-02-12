import React from 'react';

const Logout = props => {
  localStorage.removeItem('token');
  window.location.reload();
  props.history.push('/');
  return <div></div>;
};

export default Logout;
