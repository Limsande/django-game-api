from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import GameSerializer


@api_view(['GET', 'POST'])
def games(request: Request, format=None) -> Response:
    """
    The /games endpoint.

    Request methods:
        - GET: returns list of all games
        - POST: creates a new game
    """
    if request.method == 'GET':
        return get_games()
    if request.method == 'POST':
        return post_game(request)


def post_game(request: Request) -> Response:
    """Create a new game"""
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_games() -> Response:
    """Return list of all games"""
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request: Request, id: int, format=None) -> Response:
    """
    The /games/id endpoint, where *id* is the ID of an existing game.

    Request methods:
        - GET: returns the game
        - PUT: updates the game
        - DELETE: deletes the game
    """
    try:
        game = Game.objects.get(pk=id)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return serialize_game(game)
    if request.method == 'PUT':
        return update_game(request, game)
    if request.method == 'DELETE':
        return delete_game(game)


def serialize_game(game: Game) -> Response:
    """Serializes *game* into a Response object"""
    serializer = GameSerializer(game)
    return Response(serializer.data)


def update_game(request: Request, game: Game) -> Response:
    """Update *game*"""
    serializer = GameSerializer(game, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_game(game: Game) -> Response:
    """Delete *game*"""
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
