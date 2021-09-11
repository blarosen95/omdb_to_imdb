import logging

import attr
import requests

logger = logging.getLogger(__name__)


@attr.s(slots=True)
class CastAPI:
    config = attr.ib()
    secrets = attr.ib()
    _session = attr.ib()

    @_session.default
    def default_session(self):
        querystring = {}
        headers = {}

        if getattr(self.secrets, 'imdb_api_key'):
            querystring['api_key'] = self.secrets.imdb_api_key
        elif getattr(self.secrets, 'imdb_access_token'):
            headers = {'Authorization': f'Bearer {self.secrets.imdb_access_token}'}

        s = requests.Session()
        s.params = querystring
        s.headers = headers

        return s

    def url_builder(self, imdbID):
        api_key = self._session.params['api_key']
        return f'https://imdb-api.com/en/API/FullCast/{api_key}/{imdbID}'

    def get_fqdn(self, data):
        return self.url_builder(data)

    def _get(self, url, **kwargs):
        kwargs.setdefault('timeout', (3.05, 60))
        return self._session.get(url, **kwargs)

    def create(self, entity, data):
        logger.info(f'Attempting to create a {entity} record')
        data = self._get(self.get_fqdn(data))
        return data
