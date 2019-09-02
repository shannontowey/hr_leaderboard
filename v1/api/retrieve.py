from flask_restplus import Resource
from webargs.flaskparser import use_args

from ..schema.retrieve import Retrieve

class RetrieveAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.gamefeed_adapter = kwargs['gamefeed_adapter']
        super().__init__()

    @use_args(Retrieve())
    def post(self, args):
        hr_leaders = self.gamefeed_adapter.query_for_game_data(args)
        return hr_leaders
