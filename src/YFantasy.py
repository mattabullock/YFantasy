from YSession import YSession

def main():
	session = YSession()
	session.set_active('nhl')
	session.get_league_IDs()


if __name__ == "__main__":
    main()
