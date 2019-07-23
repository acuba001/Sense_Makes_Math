import React, { Component } from 'react'
import { connect } from 'react-redux'
import ReactHtmlParser from 'react-html-parser'

class Home extends Component {
  render() {
    const {blogger: {recentBlogPosts}} = this.props
    var i = 0
    return (
      <div className="container">
        {
          recentBlogPosts.map(post => (
            <div className="card rounded-0 mb-3" key={i++}>
              <div className="card-body">
                <h3 className="card-title">{post.title}</h3>
                <div className="card-text">
                  {ReactHtmlParser(post.content)}
                </div>
              </div>
            </div>
          ))
        }
      </div>
    )
  }
}

export default connect((state) => ({ blogger: state.blogger }))(Home)