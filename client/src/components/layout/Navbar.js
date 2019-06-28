import React, { Component } from 'react'

import shows from './images/Navbar/navi-shows.jpg'
import socialMedia from './images/Navbar/navi-social-media.jpg'
import store from './images/Navbar/navi-store.jpg'
import supportUs from './images/Navbar/navi-support-us.jpg'
import about from './images/Navbar/navi-about.jpg'

import showsGrey from './images/Navbar/navi-shows-over.jpg'
import socialMediaGrey from './images/Navbar/navi-social-media-over.jpg'
import storeGrey from './images/Navbar/navi-store-over.jpg'
import supportUsGrey from './images/Navbar/navi-support-us-over.jpg'
import aboutGrey from './images/Navbar/navi-about-over.jpg'


export default class Navbar extends Component {

  constructor(props){
    super(props)

    this.state = {
      showsHover: false,
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
      showsHover, 
      socialMediaHover, 
      storeHover, 
      supportUsHover, 
      aboutHover
    } = this.state

    const showsElem = <img 
      onMouseEnter={this.onMouseEnter.bind(this,"showsHover")} 
      onMouseLeave={this.onMouseLeave.bind(this,"showsHover")}
      src={showsHover ? showsGrey : shows} 
      alt="SHOWS"
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
      <div className="row">
        <div className="col-lg-2 text-center my-3"><a href="/" className="nounderline text-dark nohover">HOME</a></div>
        <div className="col-lg-2 text-center my-3"><a href="/shows" className="nounderline text-dark">{showsElem}</a></div>
        <div className="col-lg-2 text-center my-3"><a href="https://www.facebook.com/SenseMakesMath/" target="_blank" rel="noopener noreferrer" className="nounderline text-dark">{socialMediaElem}</a></div>
        <div className="col-lg-2 text-center my-3"><a href="http://sensemakesmath.storenvy.com/" target="_blank" rel="noopener noreferrer" className="nounderline text-dark">{storeElem}</a></div>
        <div className="col-lg-2 text-center my-3"><a href="https://www.patreon.com/sensemakesmath" target="_blank" rel="noopener noreferrer" className="nounderline text-dark">{supportUsElem}</a></div>
        <div className="col-lg-2 text-center my-3"><a href="/about" className="nounderline text-dark">{aboutElem}</a></div>
      </div>
    )
  }
}
