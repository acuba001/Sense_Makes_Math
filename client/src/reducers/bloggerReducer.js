import { GET_BLOGGER_POSTS } from '../actions/types'

const initialState = {
  recentBlogPosts: [
    {
      "content": "<br />\n<div class=\"MsoNormal\">\nMost people would tell you that \u201cmath does not make sense\u201d\nand self-described \u201cmath people\u201d usually take offense to that. However: most\npeople are correct! </div>\n<div class=\"MsoNormal\">\nSense Makes Math is a community where we all agree that Math\nDoes Not Make Sense: Sense Makes Math. Sense is a verb: YOU <i>make sense</i>\nOUT OF Mathematics by using your mind/attention/Logos. Investigating\nmathematical objects is a journey through the collective imagination of\nhumankind and is something you can only do for yourself.</div>\n<div class=\"MsoNormal\">\nOur Mission is to expose the world to the Beauty, Power, and\nMagic that is the sacred art of Mathematicians.</div>\n<br />", 
      "title": "Welcome to SenseMakesMath.com" 
    }
  ]
}

export default (state = initialState, action) => {
  switch (action.type) {
    case GET_BLOGGER_POSTS:
      return state
    default:
      return state
  }
}