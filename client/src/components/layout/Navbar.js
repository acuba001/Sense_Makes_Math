import React, { Component } from 'react'

import home from './images/Navbar/navi-home.jpg'
import shows from './images/Navbar/navi-shows.jpg'
import podcast from './images/Navbar/navi-podcast.jpg'
import socialMedia from './images/Navbar/navi-social-media.jpg'
import store from './images/Navbar/navi-store.jpg'
import supportUs from './images/Navbar/navi-support-us.jpg'
import about from './images/Navbar/navi-about.jpg'

import homeGrey from './images/Navbar/navi-home-over.jpg'
import showsGrey from './images/Navbar/navi-shows-over.jpg'
import podcastGrey from './images/Navbar/navi-podcast-over.jpg'
import socialMediaGrey from './images/Navbar/navi-social-media-over.jpg'
import storeGrey from './images/Navbar/navi-store-over.jpg'
import supportUsGrey from './images/Navbar/navi-support-us-over.jpg'
import aboutGrey from './images/Navbar/navi-about-over.jpg'


export default class Navbar extends Component {

  constructor(props){
    super(props)

    this.state = {
      homeHover: false,
      showsHover: false,
      podcastHover: false,
      socialMediaHover: false,
      storeHover: false,
      supportUsHover: false,
      aboutHover: false
    }
  }

  onMouseEnter = (navButton) => {
    this.setState({[navButton]: true})
  }

  onMouseLeave = (navButton) => {
    this.setState({[navButton]: false})
  }

  render() {

    const {
      homeHover,
      showsHover, 
      podcastHover,
      socialMediaHover, 
      storeHover, 
      supportUsHover, 
      aboutHover
    } = this.state

    const homeElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"homeHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"homeHover")}
      src={homeHover ? homeGrey : home} 
      alt="HOME"
    />

    const showsElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"showsHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"showsHover")}
      src={showsHover ? showsGrey : shows} 
      alt="SHOWS"
    />

    const podcastElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"podcastHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"podcastHover")}
      src={podcastHover ? podcastGrey : podcast} 
      alt="PODCAST"
    />

    const socialMediaElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"socialMediaHover")} 
      onMouseLeave={this.onMouseLeave.bind(this, "socialMediaHover")}
      src={socialMediaHover ? socialMediaGrey : socialMedia} 
      alt="SOCIAL MEDIA"
    />
    const storeElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"storeHover")} 
      onMouseLeave={this.onMouseLeave.bind(this, "storeHover")}
      src={storeHover ? storeGrey : store} 
      alt="STORE"
    />
    const supportUsElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"supportUsHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"supportUsHover")} 
      src={supportUsHover ? supportUsGrey : supportUs} 
      alt="SUPPORT US"
    />
    const aboutElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"aboutHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"aboutHover")} 
      src={aboutHover ? aboutGrey : about} 
      alt="ABOUT"
    />

    return (
      <nav className="navbar navbar-expand-lg navbar-light">
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarDropdownContent" aria-controls="navbarDropdownContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarDropdownContent">
          <ul className="navbar-nav m-auto">
          <li className="nav-item">
               <a href="/" className="nav-link nounderline text-dark">{homeElem}</a>
             </li>
             <li className="nav-item">
               <a href="/shows" className="nav-link nounderline text-dark">{showsElem}</a>
             </li>
             <li className="nav-item">
               <a href="/podcast" className="nav-link nounderline text-dark">{podcastElem}</a>
             </li>
             <li className="nav-item">
               <a href="https://twitter.com/sensemakesmath" target="_blank" rel="noopener noreferrer" className="nav-link nounderline text-dark">{socialMediaElem}</a>
             </li>
             <li className="nav-item">
               <a href="http://sensemakesmath.storenvy.com/" target="_blank" rel="noopener noreferrer" className="nav-link nounderline text-dark">{storeElem}</a>
             </li>
             <li className="nav-item">
               <a href="https://www.patreon.com/sensemakesmath" target="_blank" rel="noopener noreferrer" className="nav-link nounderline text-dark">{supportUsElem}</a>
             </li>
             <li className="nav-item">
               <a href="/about" className="nav-link nounderline text-dark">{aboutElem}</a>
             </li>
          </ul>
        </div>
      </nav>
    )
  }
}