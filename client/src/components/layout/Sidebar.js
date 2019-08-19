import React, { Component } from 'react'
import { connect } from 'react-redux'
import {getYouTubeVideos} from '../../actions/youtubeActions'

import classNames from 'classnames'

import pic1 from './images/Sidebar/RYS-all-Advertisement.jpg'
import pic2 from './images/Sidebar/RYS-empty-Advertisement.jpg'
import pic3 from './images/Sidebar/RYS-N-Advertisement.jpg'
import pic4 from './images/Sidebar/RYS-Z-Advertisement.jpg'
import pic5 from './images/Sidebar/RYS-Q-Advertisement.jpg'
import pic6 from './images/Sidebar/RYS-R-Advertisement.jpg'
import pic7 from './images/Sidebar/RYS-C-Advertisement.jpg'

import loadingSpinner from './images/Sidebar/kloader.gif'

class Sidebar extends Component {

  componentDidMount(){
    this.props.getYouTubeVideos()
  }

  render() {
    const { recentVideos } = this.props
    const latestVideo = recentVideos ? recentVideos[0] : null
    const latestVideoId = latestVideo ? latestVideo.id : null
    const latestVideoClasses = classNames({
      "card-body": true,
      "embed-responsive": latestVideo,
      "embed-responsive-16by9": latestVideo
    })
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
          <div className={latestVideoClasses}>
            {latestVideo ? 
              (<iframe className="embed-responsive-item" title={latestVideoId} src={'https://www.youtube.com/embed/' + latestVideoId} allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>)
              : (<img className="d-block mx-auto" style={{width: "10%"}} src={loadingSpinner} alt="Loading Latest Video" />)
            }
          </div>
        </div>
        {/* TODO: For advertising latest podcast */}
        {/* <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>PODCAST</h4>
          </div>
        </div> */}
        <div className="card rounded-0 mb-3">
          <div className="card-header text-center">
            <h4>ADVERTISEMENT</h4>
            <div id="carouselExampleIndicators" className="carousel slide" data-ride="carousel">
              <ol className="carousel-indicators">
                <li data-target="#carouselExampleIndicators" data-slide-to="0" className="active"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="3"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="4"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="5"></li>
                <li data-target="#carouselExampleIndicators" data-slide-to="6"></li>
              </ol>
              <div className="carousel-inner">
                <div className="carousel-item active">
                  <img className="d-block w-100" src={pic1} alt="First slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic2} alt="Second slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic3} alt="Third slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic4} alt="Fourth slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic5} alt="Fifth slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic6} alt="Sixth slide" />
                </div>
                <div className="carousel-item">
                  <img className="d-block w-100" src={pic7} alt="Seventh slide" />
                </div>
              </div>
              <a className="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                <span className="sr-only">Previous</span>
              </a>
              <a className="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                <span className="carousel-control-next-icon" aria-hidden="true"></span>
                <span className="sr-only">Next</span>
              </a>
            </div>
            <a href="http://sensemakesmath.storenvy.com/" className="btn btn-light btn-block" target="_blank" rel="noopener noreferrer">
              Head Over To Our Shop Now!
            </a>
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
            <a href="www.youtube.com/sensemakesmath" className="btn btn-light border border-secondary boarder-rounded-0" target="_blank" rel="noopener noreferrer">
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

const mapStateToProps = state => ({
  recentVideos: state.youtube.recentVideos 
}) 

export default connect(mapStateToProps, {getYouTubeVideos})(Sidebar)
