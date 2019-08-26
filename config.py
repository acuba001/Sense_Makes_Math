import os

class Config(object):
    #########################
    #   REQUIRED SETTINGS   #
    #########################

    # Blogger
    BLOGGER_PAGE_BLOG_ID=os.environ.get('BLOGGER_PAGE_BLOG_ID')

    # Cache
    CACHE_TYPE=os.environ.get('CACHE_TYPE') or 'simple'

    # Google
    GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY') 

    # Facebook
    FACEBOOK_APP_ID=os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_API_VERSION=os.environ.get('FACEBOOK_API_VERSION')

    # PayPal
    PAYPAL_MODE=os.environ.get('PAYPAL_MODE') or 'live'
    PAYPAL_CLIENT_ID=os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET=os.environ.get('PAYPAL_CLIENT_SECRET')

    # Printful
    PRINTFUL_STORE_ID=os.environ.get('PRINTFUL_STORE_ID')
    PRINTFUL_API_KEY= os.environ.get('PRINTFUL_API_KEY')

    # Spotify
    SPOTIFY_CLIENT_ID=os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET=os.environ.get('SPOTIFY_CLIENT_SECRET')

    # YouTube
    YOUTUBE_CHANNEL_ID=os.environ.get('YOUTUBE_CHANNEL_ID')
   
    #########################
    #   OPTIONAL SETTINGS   #
    #########################

    # Blogger
    BLOGGER_DATA_FETCH_PER_DAY=int(os.environ.get('BLOGGER_DATA_FETCH_PER_DAY') or 15)

    # Facebook
    FACEBOOK_DATA_FETCH_PER_DAY=int(os.environ.get('FACEBOOK_DATA_FETCH_PER_DAY') or 48)
    FACEBOOK_DATA_MAXRESULTS=int(os.environ.get('FACEBOOK_DATA_MAXRESULTS') or 10)

    # Printful
    PRINTFUL_DATA_FETCH_PER_DAY=int(os.environ.get('PRINTFUL_DATA_FETCH_PER_DAY') or 48)
    PRINTFUL_DATA_MAXRESULTS=int(os.environ.get('PRINTFUL_DATA_MAXRESULTS') or 10)

    # YouTube
    YOUTUBE_DATA_FETCH_PER_DAY=int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY') or 48)
    YOUTUBE_DATA_MAXRESULTS=int(os.environ.get('YOUTUBE_DATA_MAXRESULTS') or 10)