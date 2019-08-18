import React, { Component } from 'react'
import { connect } from 'react-redux'
import {getYouTubeVideos} from '../../actions/youtubeActions'

class Shows extends Component {
  componentDidMount(){
    this.props.getYouTubeVideos()
  }

  render() {
    const { youtube: { recentVideos } } = this.props
    return (
      <div className="container p-3">
        {recentVideos
          .filter((video, ind) => ind < process.env.REACT_APP_SHOWS_NUM)
          .map((video, ind) => (
            <div key={ind} className="embed-responsive embed-responsive-16by9 mb-3">
              <iframe className="embed-responsive-item" title={video.id} src={'https://www.youtube.com/embed/' + video.id} allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
            </div>
          ))
        }
        <a href="https://www.youtube.com/channel/UCI3K1J8do2RAa0wC60YGK5Q" className="btn btn-light btn-block" target="_blank" rel="noopener noreferrer">
          Click Here For More!
        </a>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  youtube: state.youtube 
}) 

export default connect(mapStateToProps, {getYouTubeVideos})(Shows)
