import { GET_YOUTUBE_VIDEOS } from '../actions/types'

const initialState = {
  recentVideos: []
}

export default (state=initialState, action) => {
  switch (action.type) {
    case GET_YOUTUBE_VIDEOS:
      return {
        ...state,
        recentVideos: action.payload
      }
    default:
      return state
  }
}