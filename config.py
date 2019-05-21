import os

class Config(object):
    
    # REQUIRED
    GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY') 
    FACEBOOK_APP_ID=os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_API_VERSION=os.environ.get('FACEBOOK_API_VERSION')
    
    # OPTIONAL
    YOUTUBE_DATA_FETCH_PER_DAY=int(os.environ.get('YOUTUBE_DATA_FETCH_PER_DAY') or 48)
    YOUTUBE_CHANNEL_ID=os.environ.get('YOUTUBE_CHANNEL_ID') or 'UCI3K1J8do2RAa0wC60YGK5Q'
    YOUTUBE_DATA_MAXRESULTS=int(os.environ.get('YOUTUBE_DATA_MAXRESULTS') or 10)
    CACHE_TYPE=os.environ.get('CACHE_TYPE') or 'simple'