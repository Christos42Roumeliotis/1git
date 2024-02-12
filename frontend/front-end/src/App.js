import Layout from './components/Layout/Layout';
import Home from './components/Pages/Home/Home';
import classes from './components/Layout/Layout.module.css';
import { Route } from 'react-router-dom';
import Endpoints from './containers/Endpoints/Endpoints';
import Login from './containers/Login/Login';
import Logout from './containers/Login/Logout';
import Passesperstation from './containers/Endpoints/Passesperstation';
import About from './components/Pages/About/About';
import PassesAnalysis from './containers/Endpoints/PassesAnalysis';
import PassesCost from './containers/Endpoints/PassesCost';
import Chargesby from './containers/Endpoints/Chargesby';



function App() {
  return (
    <div>
      <Layout classname={classes.Layout}>
        <Route path="/" exact component={Home} />
        <Route path="/passesperstation" exact component={Passesperstation}></Route>
        <Route path="/passesanalysis" exact component={PassesAnalysis}></Route>
        <Route path="/passescost" exact component={PassesCost}></Route>
        <Route path="/chargesby" exact component={Chargesby}></Route>
        <Route path="/endpoints" exact component={Endpoints} />
        <Route path="/login" exact component={Login} />
        <Route path="/about" exact component={About} />
        <Route path="/logout" exact component={Logout} />
      </Layout>
    </div>
  );
}

export default App;
