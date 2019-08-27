import React from 'react'

import applePodcast from './images/Podcast/Apple_Podcast_Icon.png'
import spotifyPodcast from './images/Podcast/Spotify_Icon_CMYK_Green.png'
import googlePodcast from './images/Podcast/google_podcasts_icon_badge@3x.png'

export default function Podcast() {
  return (
    <>
      <div className="embed-responsive embed-responsive-4by3">
          <iframe id="player_iframe" title="Podcast Widget" src="https://www.buzzsprout.com/301124?client_source=small_player&amp;iframe=true&amp;referrer=https://www.buzzsprout.com/301124.js?player=small" className="embed-responsive-item" scrolling="no"></iframe>
      </div>
      <div className="row d-flex justify-content-center m-3">
        <div className="col-8">
          <p className="lead">Our podcast is also available at:</p>
        </div>
      </div>
      <div className="row d-flex justify-content-center">
        <ul className="list-inline col-6">
          <li className="list-inline-item">
            <a href="https://podcasts.apple.com/us/podcast/sense-makes-math-presents-meet-a-mathematician/id1462376460?uo=4" className="text-dark" target="_blank" rel="noopener noreferrer">
              <span className="mr-3"><img src={applePodcast} className="img-fluid mb-3" style={{width: "20%"}} alt="Apple Podcast"/></span>iTunes
            </a>
          </li>

          <li className="list-inline-item">
            <a href="https://open.spotify.com/show/0hxsSzaQK5k5aet8nmsK34" className="text-dark" target="_blank" rel="noopener noreferrer">
              <span className="mr-3"><img src={spotifyPodcast} className="img-fluid mb-3" style={{width: "20%"}} alt="Spotify"/></span>Spotify
            </a>
          </li>

          <li className="list-inline-item">
            <a href="https://podcasts.google.com/?feed=aHR0cHM6Ly9mZWVkcy5idXp6c3Byb3V0LmNvbS8zMDExMjQucnNz" className="text-dark" target="_blank" rel="noopener noreferrer">
              <span className="mr-3"><img src={googlePodcast} className="img-fluid" style={{width: "20%"}} alt="Google Podcast"/></span>Google Podcast
            </a>
          </li>
        </ul>
      </div>
    </>
  )
}
