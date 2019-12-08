#!/usr/bin/python

hostname = '10.100.71.21'
username = '201701068'
password = '1234'
database = '201701068'

import psycopg2
from tabulate import tabulate
try:
	conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
	conn.autocommit = True
except:
	print("'Could'nt connect to database")
flag=0
while flag!=1:
	print("--------------------------------------------")
	print("                IPL DATABASE                ")
	print("--------------------------------------------")
	print("Enter your choice ->")
	print("1.Query the database")
	print("2.Insert into the database")
	print("3.Exit the app")
	cur=conn.cursor()
	cur.execute("SET SEARCH_PATH TO IPL;")
	n=int(input())
	if n==1:
		print("--------------------------------------------")
		print("Enter your choice ->")
		print("1.General Player statistics")
		print("2.General Team statistics")
		print("3.Match statistic")
		print("4.Season statistic")
		print("5.Given a venue what is better chasing or defending")
		print("6.Total how many match results were decided by superover through the course of IPL till 2016")
		print("7.Name the venue and the city where the team that won the toss also won the match for max no. of times")
		print("8.Name the Best Fielders in IPL history interms of number of catches caught")
		print("9 To make a custom query (Note: Only SELECT queries are allowed")
		a=int(input())
		if a==1:
			print("Enter your choice ->")
			print("1.List all Players in the IPL")
			print("2.Individual Player Statistics") 
			print("3.List the players who have scored Centuries in a match in IPL history")
			print("4.List the players who have taken 5-wicket hauls in IPL history")
			b=int(input())
			if b==1:
				print("All players")
				cur.execute("SELECT * FROM players")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Player_id','Player_name','Bowling_hand','Batting_Type','DOB','Country','Runs_Scores','Wickets','Catches'], tablefmt='psql'))
			if b==2:
				print("Enter the name of the player for his statistics")
				player=input()
				cur.execute(f"SELECT * FROM Players WHERE player_name='{player}';")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Player_id','Player_name','Bowling_hand','Batting_Type','DOB','Country','Runs_Scores','Wickets','Catches'], tablefmt='psql'))
			elif b==3:
				cur.execute("SELECT DISTINCT player_name,count(sum) FROM (SELECT match_id,striker,sum(batsman_score) FROM ball_by_ball GROUP BY match_id,striker \
								HAVING sum(batsman_score)>=100 )as c JOIN players ON striker=player_id GROUP BY player_name;")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Player_name','Num_of_Centuries'], tablefmt='psql'))
			elif b==4:
				cur.execute("SELECT player_name,COUNT(COUNT) AS five_wicket_hauls FROM players JOIN \
					(SELECT match_id,bowler,COUNT(dismissal_type) FROM ball_by_ball \
					 WHERE dismissal_type!='run out' AND dismissal_type!=' ' AND dismissal_type!='retired hurt' \
					 GROUP BY match_id,bowler HAVING COUNT(dismissal_type)=5) AS r \
					 ON bowler=player_id GROUP BY player_name;")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Player_name','Num_of_fifers'], tablefmt='psql'))
		if a==2:
			print("Enter your choice ->")
			print("1.Individual Team Statistics")
			print("2.Players of that Team in a given season")
			c=int(input())
			if c==1:
				print("Enter the name of the Team for It's statistics")
				team=input()
				cur.execute(f"select team_id,team_name,team_code,count from teams join (select wining_team_id,count(wining_team_id) from match where wining_team_id is not NULL group by wining_team_id) as r on team_id=wining_team_id where team_name='{team}';")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Team_ID','Team_Name','Team_Code','Num_of_Wins'], tablefmt='psql'))
			elif c==2:
				print("Enter the season number and the team Id")
				season=int(input())
				teamid=int(input())
				cur.execute(f"select distinct h.player_id,player_name,teams.team_name from has_played as h join match as m on h.match_id=m.match_id join teams on h.team_id=teams.team_id join players on h.player_id=players.player_id where season_id='{season}' and teams.team_id={teamid};")
				rows=cur.fetchall()
				print(tabulate(rows, headers=['Player_Id','Player_name','Team_name'], tablefmt='psql'))
		if a==3:
			print("Individual Match Statistics")
			print("The teams in the IPL history")
			cur.execute("SELECT * FROM Teams")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Team_ID','Team_Name','Team_Code'], tablefmt='psql'))
			print("Enter the team id's of the 2 Teams for the match")
			team_id_1=input()
			team_id_2=input()
			cur.execute(f"select team_Id_1,team_Id_2,Match_Date,Venue_Name,Is_Result,Is_superover,Team1_Score,Team2_score,Team_1_wickets,Team_2_Wickets,Win_Type,Won_by,Wining_Team_Id from match where (team_id_1={team_id_1} and team_id_2={team_id_2}) or (team_id_1={team_id_2} and team_id_2={team_id_1});")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Team1','Team2','Date','Venue','Result','Superover','Team1_Score','Team2_Score','Team1_Wickets','Team2_Wickets','Win_Type','Won_by','Winning_Team'], tablefmt='psql'))
		if a==4:
			print("Individual Season Statistics")
			print("Enter the season id of whose statistics you want")
			season=input()
			cur.execute(f"select seasons.season_id,season_year,e.player_name as orange_cap,f.player_name as purple_cap,g.player_name as man_of_the_tournament,team_name as winning_team from seasons join match on match.season_id=seasons.season_id join teams on team_id=wining_team_id join players as e on e.player_id=orange_cap join players as f on f.player_id=purple_cap join players as g on g.player_id=man_of_the_series where seasons.season_id={season} order by match_id DESC limit 1;")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Season_No.','Year','Man_Of_The_Tournament','Purple_Cap','Orange_Cap','Winning_Team'], tablefmt='psql'))
		if a==5:
			print("Enter the venue whose statistics you want")
			venue=input()
			cur.execute(f"select venues.venue_name,count(wining_team_id) from venues join match on venues.venue_name=match.venue_name where venues.venue_name='{venue}' and (toss_won_by=wining_team_id and toss_descision='bat') group by venues.venue_name;")
			rows=cur.fetchall()
			a,b=rows[0]
			cur.execute(f"select venues.venue_name,count(wining_team_id) from venues join match on venues.venue_name=match.venue_name where venues.venue_name='{venue}' and (toss_won_by=wining_team_id and toss_descision='field') group by venues.venue_name;")
			rows=cur.fetchall()
			c,d=rows[0]
			print(f"Batting First : {b} wins")
			print(f"Bowling FIrst : {d} wins")
		if a==6:
			cur.execute("SELECT COUNT(match_id) FROM match WHERE is_superover='true'");
			rows=cur.fetchall()
			print(f"Number of matches decided by superover is {rows[0][0]}")
		if a==7:
			cur.execute("SELECT venues.venue_name,city.city_name FROM res1 JOIN venues ON res1.venue_name=venues.venue_name JOIN city on venues.city_id=city.city_id ORDER BY match_won DESC LIMIT 1;")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Venue_Name','City_Name'], tablefmt='psql'))
		if a==8:
			cur.execute("select COUNT(fielder_id) AS tot,player_name FROM ball_by_ball JOIN players ON fielder_id=player_id WHERE dismissal_type='caught' GROUP BY player_name ORDER BY tot DESC LIMIT 5;")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Catches','Player_Name'], tablefmt='psql'))
		if a==9:
			print("Enter your select query string")
			query=input()
			cur.execute(query)
			rows=cur.fetchall()
			print(tabulate(rows, tablefmt='psql'))
	elif n==2:
		print("Enter your choice ->")
		print("1.Add a New Team")
		print("2.Add a New Player")
		print("3.Add a New Venue")
		print("Enter your choice")
		d=int(input())
		if d==1:
			cur.execute("SELECT * FROM Teams ORDER BY team_id DESC LIMIT 1")
			rows=cur.fetchall()
			team_id=rows[0][0]+1
			print("Enter Team_Name")
			team_name=input()
			print("Enter Team_Code")
			team_code=input()
			cur.execute(f"INSERT INTO teams VALUES({team_id},'{team_name}','{team_code}');")
			print("Insertion Completed")
		elif d==2:
			cur.execute("SELECT * FROM players ORDER BY player_id DESC LIMIT 1")
			rows=cur.fetchall()
			player_id=rows[0][0]+1
			print("Enter Player_Name")
			player_name=input()
			print("Enter Bowling_hand")
			bowling_hand=input()
			print("Enter Batting_type")
			batting_type=input()
			print("Enter the Date of birth in yyyy-mm-dd format")
			dob=input()
			print("Enter the player's country")
			country=input()
			print("Enter the player's score")
			score=input()
			print("Enter the player's wickets")
			wickets=input()
			print("Enter the player's catches")
			catches=input()
			cur.execute(f"INSERT INTO players VALUES({player_id},'{player_name}','{bowling_hand}','{batting_type}','{dob}','{country}','{score}','{wickets}','{catches}');")
			print("Insertion Completed")
		elif d==3:
			print("Look up the city table for city_id for Venues ")
			cur.execute("SELECT * FROM city")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['City_Id','City_name','State_name','Country'], tablefmt='psql'))
			print("Look up the teams table for team_id for Venues ")
			cur.execute("SELECT * FROM Teams")
			rows=cur.fetchall()
			print(tabulate(rows, headers=['Team_ID','Team_Name','Team_Code'], tablefmt='psql'))
			print("Enter Venue_Name")
			venue=input()
			print("Enter Home_Team_Id")
			Home_Team_Id=input()
			print("Enter City_Id")
			City_Id=input()
			cur.execute(f"INSERT INTO Venues VALUES('{venue}','{Home_Team_Id}','{City_Id}');")
			print("Insertion Completed")
	elif n==3:
		print("Thank you for using the database")
		flag=1;
	else:
		print("Invalid input, Enter choice between 0 and 3")
