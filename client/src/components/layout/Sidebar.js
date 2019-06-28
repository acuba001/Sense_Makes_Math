import React, { Component } from 'react'
import {connect} from 'react-redux'

class Sidebar extends Component {
  render() {
    const {latestVideo} = this.props
    return (
      <div className="container">
        <br />
        <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>LATEST TWEET</h4>
          </div>
          <div className="card-body">
            <a className="twitter-timeline" href="https://twitter.com/SenseMakesMath?ref_src=twsrc%5Etfw" data-tweet-limit="1">Latest Tweet by SenseMakesMath</a>
          </div>
        </div>
        <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>LATEST VIDEO</h4>
          </div>
          <div className="card-body embed-responsive embed-responsive-16by9">
              <iframe className="embed-responsive-item" title={latestVideo} src={'https://www.youtube.com/embed/' + latestVideo} allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
          </div>
        </div>
        <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>PODCAST</h4>
          </div>
        </div>
        <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>ADVERTISEMENT</h4>
          </div>
        </div>
          <div className="d-flex justify-content-around">
            <div className="p-2">
              <a href="https://www.patreon.com/sensemakesmath" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-patreon"></i>
              </a>
            </div>
            <div className="p-2">
              <a href="https://twitter.com/sensemakesmath" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-twitter"></i>
              </a>
            </div>
            <div className="p-2">
              <a href="https://www.facebook.com/SenseMakesMath/" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-facebook"></i>
              </a>
            </div>
            <div className="p-2">
              <a href="https://www.youtube.com/channel/UCI3K1J8do2RAa0wC60YGK5Q" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-youtube"></i>
              </a>
            </div>
            <div className="p-2">
              <a href="https://open.spotify.com/show/0hxsSzaQK5k5aet8nmsK34" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
                <i className="fab fa-spotify"></i>
              </a>
            </div>
          </div>
      </div>
    )
  }
}

export default connect((state) => ({ latestVideo: state.youtube.recentVideos[0] }))(Sidebar)