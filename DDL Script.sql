  SET SEARCH_PATH TO IPL;


  CREATE TABLE City (
   	  	City_Id SMALLINT PRIMARY KEY,
      		City_Name TEXT NOT NULL UNIQUE,
   	  	State_Name TEXT NOT NULL,
   	  	Country TEXT NOT NULL
    );
  CREATE TABLE Umpires (
   		Umpire_Id SMALLINT PRIMARY KEY,
   		Umpire_Name TEXT NOT NULL,
  		Country TEXT NOT NULL
   );
  CREATE TABLE Sponsors (
   		Sponsor_Id SMALLINT PRIMARY KEY,
   		Sponsor_Name TEXT NOT NULL UNIQUE
   );
  CREATE TABLE Players (
   		Player_Id SMALLINT PRIMARY KEY,
  		Player_Name TEXT NOT NULL,
  		Bowling_Hand TEXT NOT NULL,
  		Batting_Type TEXT NOT NULL,
  		DOB DATE NOT NULL,
  		Country TEXT NOT NULL,
      		Score SMALLINT DEFAULT 0,
      		Wickets SMALLINT DEFAULT 0,
      		Catches SMALLINT DEFAULT 0
   );
  CREATE TABLE Teams (
    		Team_Id SMALLINT PRIMARY KEY,
    		Team_Name TEXT NOT NULL UNIQUE,
  		Team_Code SMALLINT NOT NULL UNIQUE,
    );
  CREATE TABLE Seasons (
    		Season_Id SMALLINT PRIMARY KEY,
   		Season_Year SMALLINT NOT NULL UNIQUE,
    		Man_Of_The_Series SMALLINT NOT NULL UNIQUE REFERENCES Players(Player_Id),
    		Orange_Cap SMALLINT NOT NULL UNIQUE REFERENCES Players(Player_Id),
  		Purple_Cap SMALLINT NOT NULL UNIQUE REFERENCES Players(Player_Id)
    );
  CREATE TABLE Current_Standings (
   		Place SMALLINT,
   		Season_Id SMALLINT REFERENCES Seasons(Season_Id),
   		Team_Id SMALLINT REFERENCES Teams(Team_Id),
   		Matches_Played SMALLINT,
    		Points SMALLINT,
    		Net_Run_Rate REAL,
   		PRIMARY KEY(Season_Id,Team_Id)
   );
  CREATE TABLE Owners (
 		Owner_Id SMALLINT PRIMARY KEY,
 		Owner_Name TEXT NOT NULL,
 		Team_Id SMALLINT NOT NULL REFERENCES Teams(Team_Id)
  );
  CREATE TABLE Supporting_Staff (
    		Staff_Id SMALLINT PRIMARY KEY,
      		Staff_Name TEXT NOT NULL,
  		Supporting_Role TEXT NOT NULL,
      		Team_Id SMALLINT REFERENCES Teams(Team_Id)
  );
  CREATE TABLE Sponsored_By (
      		Team_Id SMALLINT REFERENCES Teams(Team_Id), 
  		Sponsor_Id SMALLINT NOT NULL REFERENCES Sponsors(Sponsor_Id),
  		PRIMARY KEY(Team_Id,Sponsor_Id)
   );
  CREATE TABLE Venues (
    		Venue_Name TEXT PRIMARY KEY,
    		Home_Team_Id SMALLINT NOT NULL REFERENCES Teams(Team_Id),
   		City_Id SMALLINT NOT NULL REFERENCES City(City_Id)
    );
  CREATE TABLE Plays_For (
     		Player_Id SMALLINT REFERENCES Players(Player_Id),
    		Team_Id SMALLINT NOT NULL REFERENCES Teams(Team_Id),
 		PRIMARY KEY(Player_Id,Team_Id)
     );
  
  CREATE TABLE Match (
    		Match_Id BIGINT PRIMARY KEY,
    		Season_Id SMALLINT NOT NULL REFERENCES Seasons(Season_Id),
    		Team_Id_1 SMALLINT NOT NULL REFERENCES Teams(Team_Id),
    		Team_Id_2 SMALLINT NOT NULL REFERENCES Teams(Team_Id),
    		Match_Date DATE NOT NULL,
    		Venue_Name TEXT NOT NULL REFERENCES Venues(Venue_Name),
    		Toss_Won_By SMALLINT,
    		Toss_Descision TEXT,
  		Is_Superover BOOL NOT NULL,
  		Is_DWL BOOL NOT NULL,
  		Is_Result BOOL NOT NULL,
  		Win_Type TEXT,
  		Won_By SMALLINT,
  		Wining_Team_ID SMALLINT,
  		Man_Of_The_Match SMALLINT REFERENCES Players(Player_Id),
  		Umpire_Id_1 SMALLINT NOT NULL REFERENCES Umpires(Umpire_Id),
  		Umpire_Id_2 SMALLINT NOT NULL REFERENCES Umpires(Umpire_Id),
		Team1_Score SMALLINT DEFAULT 0,
		Team2_Score SMALLINT DEFAULT 0,
		Team_1_Wickets SMALLINT DEFAULT 0,
		Team_2_Wickets SMALLINT DEFAULT 0
    );
  CREATE TABLE Has_Played (
      		Match_Id BIGINT REFERENCES Match(Match_Id),
      		Player_Id SMALLINT NOT NULL,
      		Team_Id SMALLINT NOT NULL,
      		Is_Keeper BOOL NOT NULL,
      		Is_Captain BOOL NOT NULL,
      		PRIMARY KEY(Match_Id,Player_Id,Team_Id),
      		FOREIGN KEY(Player_Id,team_Id) REFERENCES Plays_For(Player_Id,Team_Id)
     );
  CREATE TABLE Ball_By_Ball (
		Match_Id BIGINT NOT NULL REFERENCES Match(Match_Id),
		Innings_Id SMALLINT NOT NULL,
		Over_Id SMALLINT NOT NULL,
		Ball_Id SMALLINT NOT NULL,
		Striker SMALLINT NOT NULL REFERENCES Players(Player_Id),
		Non_Striker SMALLINT NOT NULL REFERENCES Players(Player_Id),
		Bowler SMALLINT NOT NULL REFERENCES Players(Player_Id),
		Batsman_Score SMALLINT NOT NULL,
		Extra_Type TEXT,
		Extra_Runs SMALLINT,
		Dismissal_Type TEXT,
		Fielder_Id SMALLINT DEFAULT NULL REFERENCES Players(Player_Id),
		PRIMARY KEY(Match_Id,Innings_Id,Over_Id,Ball_Id)
    );
