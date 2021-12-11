import os


class Config:
    """
    Contains the configuration of this program.
    """
    def __init__(self, google_client_config, track_calendars, working_hours_calendars, token_file):
        self.google_client_config = google_client_config
        self.track_calendars = track_calendars
        self.working_hours_calendars = working_hours_calendars
        self.token_file = token_file


def get_client_config_from_env():
    """
    Create a Google-format client configuration from environment variables.
    Returns: Mapping[str, Any]

    """
    return {
        'installed': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'project_id': os.getenv('GOOGLE_PROJECT_ID', ''),
            'auth_uri': os.getenv('GOOGLE_AUTH_URL', 'https://accounts.google.com/o/oauth2/auth'),
            'token_uri': os.getenv('GOOGLE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
            'auth_provider_x509_cert_url': os.getenv('GOOGLE_AUTH_PROVIDER_CERT_URL',
                                                     'https://www.googleapis.com/oauth2/v1/certs'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob', os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost')]
        }
    }


def get_calendar_list_from_env(var):
    """
    Returns a list from a comma separated string inside a environment variable
    Args:
        var: name of the env variable

    Returns: list of strings

    """
    lst = os.getenv(var, "")

    if lst is None or lst == '':
        return []

    return lst.split(',')


def get_config_from_env():
    """
    Returns a `Config` instance populated from environment variables
    Returns: Config

    """
    google_client_config = get_client_config_from_env()
    track_calendars = get_calendar_list_from_env('CALENDAR_TRACK')
    working_hours_calendars = get_calendar_list_from_env('CALENDAR_WORKTIME')
    token_file = os.getenv('TOKEN_FILE', os.path.join(os.getcwd(), 'token.json'))

    return Config(google_client_config, track_calendars, working_hours_calendars, token_file)
