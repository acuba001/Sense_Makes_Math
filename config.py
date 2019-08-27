import os

class Config(object):
    
    # REQUIRED
    GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY') 
    FACEBOOK_APP_ID=os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_API_VERSION=os.environ.get('FACEBOOK_API_VERSION')
    BLOGGER_PAGE_BLOG_ID=os.environ.get('BLOGGER_PAGE_BLOG_ID')
    SPOTIFY_CLIENT_ID=os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET=os.environ.get('SPOTIFY_CLIENT_SECRET')
    PRINTFUL_STORE_ID=os.environ.get('PRINTFUL_STORE_ID')
    PRINTFUL_API_KEY=  os.environ.get('PRINTFUL_API_KEY')
    PAYPAL_MODE=os.environ.get('PAYPAL_MODE') or 'live'
    PAYPAL_CLIENT_ID=os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET=os.environ.get('PAYPAL_CLIENT_SECRET')
    CACHE_TYPE=os.environ.get('CACHE_TYPE') or 'simple'
    
    # OPTIONAL
    FACEBOOK_DATA_MAXRESULTS=int(os.environ.get('FACEBOOK_DATA_MAXRESULTS') or 10)
    FACEBOOK_DATA_FETCH_PER_DAY=int(os.environ.get('FACEBOOK_DATA_FETCH_PER_DAY') or 48)
    BLOGGER_DATA_FETCH_PER_DAY=int(os.environ.get('BLOGGER_DATA_FETCH_PER_DAY') or 15)
    YOUTUBE_DATA_FETCH_PER_DAY=int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY') or 48)
    YOUTUBE_CHANNEL_ID=os.environ.get('YOUTUBE_CHANNEL_ID') or 'UCI3K1J8do2RAa0wC60YGK5Q'
    YOUTUBE_DATA_MAXRESULTS=int(os.environ.get('YOUTUBE_DATA_MAXRESULTS') or 10)
    # YOUTUBE_PAGE_TOKEN=os.environ.get('YOUTUBE_PAGE_TOKEN')