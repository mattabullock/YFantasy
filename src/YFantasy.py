from YSession import YSession

def main():
	session = YSession()
	games = session.get_active_games()
	print games
	leagues = session.get_leagues(games['nhl'])
	session.get_teams(leagues['The THL'])
	# session.games['nhl'].get_leagues()

if __name__ == "__main__":
    main()
