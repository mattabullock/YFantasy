from YAuth import YAuth
import json

class YSession:
	def __init__(self):
		self.session = YAuth().authorize()
		self.games = self.get_game_IDs()
		self.active = 0

	# sports are nba,nbl,mlb,nfl
	def set_active(self,sport):
		data = json.loads(self.session.get('game/'+sport, params={'format': 'json'}).content)
		key = data['fantasy_content']['game'][0]['game_key']
		if key in self.games:
			self.active = key

	# sports are nba,nhl,mlb,nfl
	def get_game_ID(self,sport):
		data = json.loads(self.session.get('game/'+sport, params={'format': 'json'}).content)
		return data['fantasy_content']['game'][0]['game_key']

	def get_game_IDs(self):
		data = json.loads(self.session.get('users;use_login=1/games', params={'format': 'json'}).content)
		game_keys = []
		games = data['fantasy_content']['users']['0']['user'][1]['games']
		for i in games.keys():
			if i != "count":
				game_keys.append(games[i]['game'][0]['game_key'])
		return game_keys

	def get_league_IDs(self):
		data = json.loads(self.session.get('users;use_login=1/games;game_keys='+self.active+'/leagues', params={'format': 'json'}).content)
		f = open('output','w')
		f.write(json.dumps(data,indent=4,separators=(',', ': ')))
