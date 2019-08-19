import React from 'react';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'

import {Provider} from 'react-redux'
import store from './store'

import banner from './website-header.jpg'
import './App.css';

import Home from './components/content/Home'
import Podcast from './components/content/Podcast'
import Shows from './components/content/Shows'
import About from './components/content/About'

import Navbar from './components/layout/Navbar'
import Sidebar from './components/layout/Sidebar'
import Footer from './components/layout/Footer'

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="bg-white">
          <img className="mx-auto mb-3 d-block img-fluid" src={banner} alt="" />
        </div>
        <div className="container mx-auto p-3">
          <p className="text-center"><span className="font-weight-bold">Our Mission:</span> To expose the world to Beauty, Power, and Magic that is the sacred art of Mathematicians</p>
          <div className="bg-white">
            <Navbar/>
            <div className="row">
              <div className="col-lg-7 m-3">
                <Switch>
                  <Route exact path="/" component={Home}/>
                  <Route exact path="/podcast" component={Podcast}/>
                  <Route exact path="/shows" component={Shows}/>
                  <Route exact path="/about" component={About}/>
                </Switch>
              </div>
              <div className="col-lg-4 m-3">
                <Sidebar/>
              </div>
            </div>
          </div>
        </div>
        <Footer/>
      </Router>
    </Provider>
  );
}

export default App;
