import React, { Component } from 'react'
import { connect } from 'react-redux'

class Shows extends Component {
  render() {
    const { youtube: { recentVideos } } = this.props
    return (
      <div className="container p-3">
        {recentVideos.map(video => (
          <div key={video} className="embed-responsive embed-responsive-16by9 mb-3">
            <iframe class="embed-responsive-item" title={video} src={'https://www.youtube.com/embed/' + video} allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
          </div>
        ))}
        <a href="https://www.youtube.com/channel/UCI3K1J8do2RAa0wC60YGK5Q" className="btn btn-light btn-block" target="_blank" rel="noopener noreferrer">
          Click Here For More!
        </a>
      </div>
    )
  }
}


export default connect((state) => ({ youtube: state.youtube }))(Shows)