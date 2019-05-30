import React from 'react';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'

import {Provider} from 'react-redux'
import store from './store'

import banner from './website-header.jpg'
import './App.css';

import Home from './components/content/Home'
import Shows from './components/content/Shows'
import About from './components/content/About'

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
            <div className="row">
              <div className="col-md-2 text-center my-3"><a href="/" className="nounderline text-dark nohover">HOME</a></div>
              <div className="col-md-2 text-center my-3"><a href="/shows" className="nounderline text-dark">SHOWS</a></div>
              <div className="col-md-2 text-center my-3"><a href="#!" className="nounderline text-dark">SOCIAL MEDIA</a></div>
              <div className="col-md-2 text-center my-3"><a href="#!" className="nounderline text-dark">STORE</a></div>
              <div className="col-md-2 text-center my-3"><a href="#!" className="nounderline text-dark">SUPPORT</a></div>
              <div className="col-md-2 text-center my-3"><a href="/about" className="nounderline text-dark">ABOUT</a></div>
            </div>
            <div className="row">
              <div className="col-lg-7 m-3">
                <Switch>
                  <Route exact path="/" component={Home}/>
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
