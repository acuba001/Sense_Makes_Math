import React, { Component } from 'react'

export default class Sidebar extends Component {
  render() {
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
        <div className="row">
          <div className="col-3">
            <a href="https://www.patreon.com/sensemakesmath" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-patreon"></i>
            </a>
          </div>
          <div className="col-3">
            <a href="https://twitter.com/sensemakesmath" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-twitter"></i>
            </a>
          </div>
          <div className="col-3">
            <a href="https://www.youtube.com/channel/UCI3K1J8do2RAa0wC60YGK5Q" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-youtube"></i>
            </a>
          </div>
          <div className="col">
            <a href="https://open.spotify.com/show/0hxsSzaQK5k5aet8nmsK34" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-spotify"></i>
            </a>
          </div>
        </div>
      </div>
    )
  }
}
