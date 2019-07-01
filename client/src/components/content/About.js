import React, { Component } from 'react'

export default class About extends Component {
  render() {
    return (
      <div className="container">
        <div className="mb-5">
          <p>
            Most people will tell you that “math does not make sense” and, in fact, most people are correct!
          </p>
          <p>
            Sense Makes Math is a community where we all agree that Math Does Not Make Sense: Sense Makes
            Math. Sense is a verb: YOU make sense OUT OF Mathematics by using your mind/attention/Logos.
            Investigating mathematical objects is a journey through the collective imagination of humankind
            and is something you can only do for yourself.
          </p>
          <p>
            Our Mission is to expose the world to the Beauty, Power, and Magic that is the sacred art of
            Mathematicians.
          </p>
          <p>
            On our <a href="https://www.youtube.com/sensemakesmath" target="_blank" rel="noopener noreferrer">YouTube channel</a>
            {' '}you will find multiple shows for all ages and backgrounds of people. We have new episodes of
            multiple shows coming out every week!
          </p>
          <p>
            We also have a podcast available on iTunes, Spotify, and Google Podcasts called Meet a
            Mathematician which releases new episodes every Monday @ 8AM EST which can also be streamed on
            our <a href="http://sensemakesmath.buzzsprout.com/" target="_blank" rel="noopener noreferrer">podcast website</a>.
          </p>
        </div>
        <dl className="row">
          <div className="col-sm-2"></div>
          <dt className="col-sm-3">Podcast</dt>
          <dd className="col-sm-6"><a href="http://sensemakesmath.buzzsprout.com" target="_blank" rel="noopener noreferrer">sensemakesmath.buzzsprout.com</a></dd>
          <div className="col-sm-1"></div>

          <div className="col-sm-2"></div>
          <dt className="col-sm-3">Twitter</dt>
          <dd className="col-sm-6"><a href="https://twitter.com/SenseMakesMath" target="_blank" rel="noopener noreferrer">@SenseMakesMath</a></dd>
          <div className="col-sm-1"></div>

          <div className="col-sm-2"></div>
          <dt className="col-sm-3">Patreon</dt>
          <dd className="col-sm-6"><a href="https://patreon.com/sensemakesmath" target="_blank" rel="noopener noreferrer">patreon.com/sensemakesmath</a></dd>
          <div className="col-sm-1"></div>

          <div className="col-sm-2"></div>
          <dt className="col-sm-3">Facebook</dt>
          <dd className="col-sm-6"><a href="https://facebook.com/SenseMakesMath" target="_blank" rel="noopener noreferrer">facebook.com/SenseMakesMath</a></dd>
          <div className="col-sm-1"></div>

          <div className="col-sm-2"></div>
          <dt className="col-sm-3">Store</dt>
          <dd className="col-sm-6"><a href="https://sensemakesmath.storenvy.com" target="_blank" rel="noopener noreferrer">sensemakesmath.storenvy.com</a></dd>
          <div className="col-sm-1"></div>
        </dl>
      </div>
    )
  }
}
