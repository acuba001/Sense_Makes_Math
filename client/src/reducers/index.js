import { combineReducers } from 'redux'
import youtubeReducer from './youtubeReducer'
import bloggerReducer from './bloggerReducer'

export default combineReducers({
  youtube: youtubeReducer,
  blogger: bloggerReducer
})