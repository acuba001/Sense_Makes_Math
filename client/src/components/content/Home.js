import React, { Component } from 'react'
import { connect } from 'react-redux'
import ReactHtmlParser from 'react-html-parser'
import {getBloggerPosts} from '../../actions/bloggerActions'
import loadingSpinner from './images/Home/kloader.gif'

class Home extends Component {

  componentDidMount(){
    this.props.getBloggerPosts()
  }

  render() {
    const {blogger: {recentBlogPosts}} = this.props
    var i = 0
    return (
      <div className="container">
        {
          recentBlogPosts.length === 0 ? 
            <img className="d-block mt-3 mx-auto" style={{width: "10%"}} src={loadingSpinner} alt="Loading Blog Posts" /> : 
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

const mapStateToProps = state => ({
  blogger: state.blogger 
})

export default connect(mapStateToProps, {getBloggerPosts})(Home)
