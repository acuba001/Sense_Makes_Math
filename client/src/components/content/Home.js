import React, { Component } from 'react'
import { connect } from 'react-redux'
import ReactHtmlParser from 'react-html-parser'
import {getBloggerPosts} from '../../actions/bloggerActions'

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
          recentBlogPosts.map(post => post.content ? (
            <div className="card rounded-0 mb-3" key={i++}>
              <div className="card-body">
                <h3 className="card-title">{post.title}</h3>
                <div className="card-text">
                  {ReactHtmlParser(post.content)}
                </div>
              </div>
            </div>
          ) : null)
        }
      </div>
    )
  }
}

const mapStateToProps = state => ({
  blogger: state.blogger 
})

export default connect(mapStateToProps, {getBloggerPosts})(Home)