import random

from rest_framework.test import APITestCase, APIRequestFactory

from games import views
from games.models import Game


def game_to_dict(game: Game) -> dict:
    return {'id': game.pk, 'title': game.title, 'studio': game.studio, 'description': game.description}


class GameApiTestCase(APITestCase):

    GAMES = [
        {'title': 'Assassin\'s Creed II', 'studio': 'Ubisoft', 'description': 'Can I climb this?'},
        {'title': 'Modern Warfare 2', 'studio': 'Infinity Ward', 'description': 'There is only one MW2!'}
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.request_factory = APIRequestFactory()

    def test_create_game(self):
        game_dict = random.choice(self.GAMES)
        request = self.request_factory.post('/games/', game_dict)
        response = views.games(request)
        try:
            game = Game.objects.get(**game_dict)
        except Game.DoesNotExist:
            self.fail('We should have the game in the db by now, but it does not exist')
        except Game.MultipleObjectsReturned:
            self.fail(f'Expected a single game in the db, but there are {Game.objects.all().count()}')

        self.assertEqual(response.data, game_to_dict(game))

    def test_retrieve_game(self):
        game = Game.objects.create(**random.choice(self.GAMES))
        request = self.request_factory.get(f'/games/{game.pk}')
        response = views.game_detail(request, id=game.pk)
        self.assertEqual(response.data, game_to_dict(game))

    def test_update_game(self):
        game_dict = random.choice(self.GAMES)
        game = Game.objects.create(**game_dict)
        game_dict['description'] = 'Updated description'
        request = self.request_factory.put(f'/games/{game.pk}', data=game_dict)
        response = views.game_detail(request, id=game.pk)
        game.refresh_from_db()
        self.assertEqual(response.data, game_to_dict(game))
        self.assertEqual(game.description, game_dict['description'])

    def test_delete_game(self):
        game_dict = random.choice(self.GAMES)
        game = Game.objects.create(**game_dict)
        request = self.request_factory.delete(f'/games/{game.pk}')
        views.game_detail(request, id=game.pk)
        self.assertRaises(Game.DoesNotExist, Game.objects.get, **game_dict)

    def test_list_games(self):
        for game in self.GAMES:
            Game.objects.create(**game)
        request = self.request_factory.get('/games/')
        response = views.games(request)
        self.assertEqual(len(response.data), len(self.GAMES))
        games_expected = Game.objects.all().order_by('title')
        for game_expected, game_actual in zip(games_expected, sorted(response.data, key=lambda x: x['title'])):
            self.assertEqual(game_actual, game_to_dict(game_expected))
