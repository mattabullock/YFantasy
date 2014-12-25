from YAuth import YAuth
from YObjects import YGame, YLeague
import json

BASE_URL = 'http://fantasysports.yahooapis.com/fantasy/v2/'

class YSession:

	def __init__(self):
		#set up session variable
		self.session = YAuth().authorize()

	def api_call(self,url):
		full_url = BASE_URL + url
		return json.loads(self.session.get(full_url, params={'format': 'json'}).content)

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
		data = self.api_call('users;use_login=1/games')
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

	'''
	League Functions

	get_leagues - get all the leagues from a certain game that the logged in
			user belongs to, returns a dictionary of YLeague objects


	'''

	def get_leagues(self,game):
		url = 'users;use_login=1/games;game_keys='+game.game_key+'/leagues'
		leagues = {}
		data = self.api_call(url)
		leagues_json = data['fantasy_content']['users']['0']['user'][1] \
						['games']["0"]['game'][1]['leagues']
		for i in leagues_json.keys():
			if i != "count":
				league_data = leagues_json[i]['league'][0]
				leagues[league_data['name']] = YLeague(
						league_data['league_type'], league_data['renewed'], 
						league_data['end_week'], league_data['name'], 
						league_data['draft_status'], league_data['league_id'], 
						league_data['start_week'], league_data['current_week'], 
						league_data['end_date'], league_data['is_pro_league'], 
						league_data['start_date'], league_data['league_update_timestamp'], 
						league_data['edit_key'], league_data['url'], 
						league_data['renew'], league_data['short_invitation_url'], 
						league_data['league_chat_id'], league_data['scoring_type'], 
						league_data['league_key'], league_data['num_teams'], 
						league_data['weekly_deadline']
					)
		return leagues

	'''
	Team Functions

	get_teams - gets all teams from a certain league, returns a dictionary
	get_active_teams - gets all teams for the logged in user, returns a dictionary

	'''

	def get_teams(self,league):
		url = 'league/'+league.league_key+'/teams'
		leagues = {}
		data = self.api_call(url)
		print json.dumps(data,sort_keys=True,indent=4,separators=(',', ': '))

		# leagues_json = data['fantasy_content']['users']['0']['user'][1] \
		# 				['games']["0"]['game'][1]['leagues']
		# for i in leagues_json.keys():
		# 	if i != "count":
		# 		league_data = leagues_json[i]['league'][0]
		# 		leagues[league_data['name']] = YLeague(
		# 				league_data['league_type'], league_data['renewed'], 
		# 				league_data['end_week'], league_data['name'], 
		# 				league_data['draft_status'], league_data['league_id'], 
		# 				league_data['start_week'], league_data['current_week'], 
		# 				league_data['end_date'], league_data['is_pro_league'], 
		# 				league_data['start_date'], league_data['league_update_timestamp'], 
		# 				league_data['edit_key'], league_data['url'], 
		# 				league_data['renew'], league_data['short_invitation_url'], 
		# 				league_data['league_chat_id'], league_data['scoring_type'], 
		# 				league_data['league_key'], league_data['num_teams'], 
		# 				league_data['weekly_deadline']
		# 			)
		# return leagues

	def get_active_teams(self):
		pass


