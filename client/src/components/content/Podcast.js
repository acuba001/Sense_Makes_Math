import React, { Component } from 'react'

export default class Podcast extends Component {
  componentDidMount(){
    // const scriptTag = document.createElement("script")
    // scriptTag.type = "text/javascript"
    // scriptTag.async = true 
    // scriptTag.src = "https://www.buzzsprout.com/301124.js?player=large"
    // scriptTag.charset = "utf-8"

    // this.instance.appendChild(scriptTag)

    console.log(unescape(decodeURI("%3Cdiv%20class=%22episode%22%3E%0A%3Ciframe%20id=%22player_iframe%22%20src=%22https://www.buzzsprout.com/301124?client_source=large_player&amp;iframe=true&amp;referrer=https%253A%252F%252Fwww.buzzsprout.com%252F301124.js%253Fplayer%253Dlarge%22%20width=%22100%25%22%20height=%22375%22%20frameborder=%220%22%20scrolling=%22no%22%3E%3C/iframe%3E%0A%3C/div%3E%0A")))
  }

  render(){
    return (
      <div className="embed-responsive embed-responsive-16by9">
        <iframe id="player_iframe" title="Podcast Widget" src="https://www.buzzsprout.com/301124?client_source=large_player&amp;iframe=true&amp;referrer=https://www.buzzsprout.com/301124.js?player=large" className="embed-responsive-item" scrolling="no"></iframe>
      </div>
    )
  }
}
