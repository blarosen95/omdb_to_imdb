import csv
import io
import sys
import logging

from omdb_pilots import OmdbAPI
from imdb_cast import CastAPI
from lib import Config, Secrets, Context, truthy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s -'
                                               '%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    config = Config.from_env()
    secrets = Secrets.from_env()
    context = Context.from_env()

    print(f'This run is in mode: {context.run_mode}', file=sys.stderr)

    omdb_api = OmdbAPI(config, secrets)
    imdb_api = CastAPI(config, secrets)

    shows_file = open('hack/exports.csv')
    # TODO: third api instantiation (maybe OneDrive CSV?)

    reader = csv.DictReader(io.TextIOWrapper(shows_file.buffer, encoding='utf-8'),
                            fieldnames=['first_name', 'last_name', 'email', 'user_id', 'favorite_show', 'address'])

    for row in reader:
        if truthy(config.make_pilot):
            logger.info(f'Creating Show: {row}')
            show_name = row['favorite_show']
            resp = omdb_api.create('show', show_name)
            resp.raise_for_status()
            imdbID = resp.json()['imdbID']

            print(imdbID)

            cast_resp = imdb_api.create('cast', imdbID)
            cast_resp.raise_for_status()
            cast = cast_resp.json()

            # TODO: Write each cast object to new CSV

    shows_file.close()


if __name__ == '__main__':
    main()
