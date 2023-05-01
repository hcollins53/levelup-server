from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer
from rest_framework.decorators import action
from django.db.models import Count, Q

class EventView(ViewSet):

    def retrieve(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        events = Event.objects.all()
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(
            attendee_count=Count('attendees'),
            joined=Count(
                'attendees',
                filter=Q(attendees=gamer)
            ))
        
        if 'game' in request.query_params:
            game = request.query_params['game']
            events = events.filter(game=game)
            # Set the `joined` property on every event
        #for event in events:
                # Check to see if the gamer is in the attendees list on the event
            #event.joined = gamer in event.attendees.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    def create(self, request):
        """Handle POST operations
            Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=gamer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        organizer = Gamer.objects.get(user=request.auth.user)
        event.organizer = organizer
        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.description = request.data["description"]
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer deleted'}, status=status.HTTP_204_NO_CONTENT)
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','name', 'game', 'organizer',
          'description', 'date_and_time', 'attendees']
class GamerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Gamer
        fields = ('id', 'full_name', 'bio')
class EventSerializer(serializers.ModelSerializer):
    organizer = GamerSerializer(many=False)
    attendee_count = serializers.IntegerField(default=None)
    class Meta:
        model = Event
        fields = ('id','name', 'game', 'organizer',
          'description', 'date_and_time', 'attendees',
          'joined', 'attendee_count')