import {GET_BLOGGER_POSTS} from './types'

export const getBloggerPosts = () => dispatch => {
  fetch(process.env.REACT_APP_FLASK_URI + '/blog-posts')
  .then(res => res.json())
  .then(data => dispatch({type: GET_BLOGGER_POSTS, payload: data.posts.reverse()}))
  .catch(e => console.error(e))
}