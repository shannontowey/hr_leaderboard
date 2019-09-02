#!flask/bin/python
import logging
import sys
import json

from flask import Flask
from flask_restplus import Api
from webargs.flaskparser import parser, abort
from flask_cors import CORS

from common.util import parse_config
from common.util import ConfigException

from v1.api.retrieve import RetrieveAPI as RetrieveAPIv1
from adapters.G2Adapter import G2Adapter


ENDPOINTS = {
    "gd2": 'gd2.mlb.com/components/'
}

def setup_adapters(config):
    adapters = dict()
    logging.debug(config['main']['mlb_endpoint'])
    adapters['gamefeed_adapter'] = G2Adapter(ENDPOINTS[config['main']['mlb_endpoint']])

    return adapters


def run_server(config):
    app = Flask(__name__)
    api = Api(app)
    if config['main']['enable_cors']:
        logging.info("Enabling CORS for all routes")
        CORS(app)

    adapters = setup_adapters(config)

    #RTT product endpoint
    api.add_resource(RetrieveAPIv1, '/v1/retrieve', '/retrieve', endpoint='v1_retrieve',
                     resource_class_kwargs={'gamefeed_adapter': adapters['gamefeed_adapter']})
    app.run(host='0.0.0.0', port=config['main']['port'], debug=config['main']['debug'])


@parser.error_handler
def handle_request_parsing_error(err, req, schema):
    try:
        json.loads(req.data)
    except ValueError:
        abort(422, error="The request parameters or data violated the schema", schema=str(err))
    abort(422, errors=err.messages)


def main():
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) != 2:
        raise ConfigException("You must specify a config file as a command-line argument")

    config_file = sys.argv[1]
    config = parse_config(config_file)

    run_server(config)


if __name__ == "__main__":
    main()
