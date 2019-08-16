import {GET_BLOGGER_POSTS} from './types'

export const getBloggerPosts = () => async dispatch => {
  const res = await fetch(process.env.REACT_APP_FLASK_URI + '/blog-posts')
  const data = await res.json()
  dispatch({type: GET_BLOGGER_POSTS, payload: data.posts.reverse()})
}