import { GET_YOUTUBE_VIDEOS } from '../actions/types'

const initialState = {
  recentVideos: [
    '01nswcUmXoE', 
    'OrFF758NhG4', 
    'QwzfjdSF924', 
    'r7DmXQJittg', 
    '6TmrMhFa4eE', 
    'CPltMqF72RU', 
    'pULA0UbhWoU', 
    '7PiDkQ6ggxY', 
    'k2oLcEgjbHA'
  ]
}

export default (state = initialState, action) => {
  switch (action.type) {
    case GET_YOUTUBE_VIDEOS:
      return state
    default:
      return state
  }
}