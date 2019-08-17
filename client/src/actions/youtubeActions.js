import {GET_YOUTUBE_VIDEOS} from './types'

export const getYouTubeVideos = () => dispatch => {
  fetch(process.env.REACT_APP_FLASK_URI + '/yt-posts')
    .then(res => res.json())
    .then(data => dispatch({type: GET_YOUTUBE_VIDEOS, payload: data.posts.reverse()}))
    .catch(e => console.error(e))
}