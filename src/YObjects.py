import json

'''
YGame - represents a Yahoo Fantasy Game associated with a professional league
'''
class YGame:

	def __init__(self,game_key,code,name,url,season,game_id,type):
		self.game_key = game_key
		self.code = code
		self.name = name
		self.url = url
		self.season = season
		self.game_id = game_id
		self.type = type

	def __str__(self):
		return self.code + " " + self.season + season + " - " + self.game_key
		
'''
YLeague - represents a Yahoo Fantasy League, contains attributes of the league
'''
class YLeague:

	def __init__(self,league_type,renewed,end_week,name,draft_status,league_id,
					start_week,current_week,end_date,is_pro_league,start_date,
					league_update_timestamp,edit_key,url,renew,short_invitation_url,
					league_chat_id,scoring_type,league_key,num_teams,weekly_deadline):
		self.league_type = league_type
		self.renewed = renewed
		self.end_week = end_week
		self.name = name
		self.draft_status = draft_status
		self.league_id = league_id
		self.start_week = start_week
		self.current_week = current_week
		self.end_date = end_date
		self.is_pro_league = is_pro_league
		self.start_date = start_date
		self.league_update_timestamp = league_update_timestamp
		self.edit_key = edit_key
		self.url = url
		self.renew = renew
		self.short_invitation_url = short_invitation_url
		self.league_chat_id = league_chat_id
		self.scoring_type = scoring_type
		self.league_key = league_key
		self.num_teams = num_teams
		self.weekly_deadline = weekly_deadline

	def __str__(self):
		return self.name

'''
YTeam - represents a Yahoo Fantasy Team
'''

class YTeam:

	def __init__():
		pass

	def __str__():
		pass