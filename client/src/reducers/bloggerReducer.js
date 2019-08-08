import { GET_BLOGGER_POSTS } from '../actions/types'

const initialState = {
  recentBlogPosts: []
}

export default (state=initialState, action) => {
  switch (action.type) {
    case GET_BLOGGER_POSTS:
      return {
        ...state,
        recentBlogPosts: action.payload
      }
    default:
      return state
  }
}