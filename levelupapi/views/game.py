from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType
from django.db.models import Count, Q
from django.core.exceptions import ValidationError


class GameView(ViewSet):
    def retrieve(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request):
        games = Game.objects.all()
        games = Game.objects.annotate(event_count=Count('events'))
        
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations
            Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateGameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'creator', 'number_of_players', 'skill_level', 'game_type']
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Gamer
        fields = ('id', 'full_name', 'bio')  
class GameSerializer(serializers.ModelSerializer):
    creator = GamerSerializer(many=False)
    event_count = serializers.IntegerField(default=None)
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_type', 'creator', 'number_of_players', 'skill_level', 'event_count')
        depth = 1