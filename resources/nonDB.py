from flask_potion import Resource, fields
from flask_potion.routes import Route


class NoDBResource(Resource):
    class Meta:
        name = 'who'

    class Schema:
        message = fields.String()

    @Route.GET
    def whos(self):
        return "hello"
