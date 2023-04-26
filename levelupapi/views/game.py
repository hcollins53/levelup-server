from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    def retrieve(self, request, pk):
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)
    def list(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations
            Returns
            Response -- JSON serialized game instance
        """
        game_type = GameType.objects.get(pk=request.data["game_type"])
        creator = Gamer.objects.get(user=request.auth.user)

        game = Game.objects.create(
            name=request.data["name"],
            creator=creator,
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            #gamer=gamer,
            game_type=game_type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.number_of_players = request.data["number_of_players"]
        game.skill_level = request.data["skill_level"]
        creator = Gamer.objects.get(user=request.auth.user)
        game.creator = creator
        game_type = GameType.objects.get(pk=request.data["game_type"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Gamer
        fields = ('id', 'full_name', 'bio')  
class GameSerializer(serializers.ModelSerializer):
    creator = GamerSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_type', 'creator', 'number_of_players', 'skill_level')
        depth = 1