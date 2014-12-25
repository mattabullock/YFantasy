from YAuth import YAuth
from YObjects import YGame, YLeague
import json

class YSession:

	def __init__(self):
		#set up session variable
		self.session = YAuth().authorize()

	def api_call(self,url):
		return json.loads(self.session.get(url, params={'format': 'json'}).content)

	'''
	Game Functions

	get_game_id - gets the the game ID for a certain sport (nhl,nba,mlb,nfl)
	get_all_games - gets all the games and returns them as a dictionary
	get_active_games - gets the games that the logged in user has a league in

	'''

	# sports are nba,nhl,mlb,nfl
	def get_game_id(self,sport):
		data = json.loads(self.session.get('game/'+sport, params={'format': 'json'}).content)
		return data['fantasy_content']['game'][0]['game_key']

	def get_all_games(self):
		data = self.api_call('games;game_keys=nfl,mlb,nba,nhl')
		games = {}
		games_json = data['fantasy_content']['games']
		for i in games_json.keys():
			if i != "count":
				game_data = games_json[i]['game'][0]
				games[game_data['code']] = YGame(
						game_data['game_key'],
						game_data['code'],
						game_data['name'],
						game_data['url'],
						game_data['season'],
						game_data['game_id'],
						game_data['type']
					)

		return games

	def get_active_games(self):
		data = json.loads(self.session.get('users;use_login=1/games', params={'format': 'json'}).content)
		games = {}
		games_json = data['fantasy_content']['users']['0']['user'][1]['games']
		for i in games_json.keys():
			if i != "count":
				game_data = games_json[i]['game'][0]
				games[game_data['code']] = YGame(
						game_data['game_key'],
						game_data['code'],
						game_data['name'],
						game_data['url'],
						game_data['season'],
						game_data['game_id'],
						game_data['type']
					)
		return games


	def get_leagues(self,game):
		url = 'users;use_login=1/games;game_keys='+game.game_key+'/leagues'
		data = self.api_call(url)
		print json.dumps(data,indent=4,separators=(',', ': '))
		# print data

	def get_nhl_leagues(self):
		return self.get_league_IDs('nhl')

	def get_nba_leagues(self):
		return self.get_league_IDs('nba')

	def get_nfl_leagues(self):
		return self.get_league_IDs('nfl')

	def get_mlb_leagues(self):
		return self.get_league_IDs('mlb')