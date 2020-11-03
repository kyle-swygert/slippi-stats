create table match (
    matchID char(50),
    stageName char(50),
    stageID integer,
    matchDate timestamp,
    gameType char(10),
    numOfFrames integer,
    fileName varchar,
    primary key(matchID)
);

create table character (
    charName char(50),
    charID char(50),
    color integer,
    didWin boolean,
    team char(5), -- the team that the player was on during a match. Will be null if the game was not a Teams match. 
    tag char(4), -- only need 4 since that is the absolute max number of chars that can be used in Melee
    portNum integer,
    cssID integer,
    primary key(charID)
    
);

-- this relation will relate all the characters that played in a specific match. 
create table character_played_in_match (

    matchID char(50),
    charID char(50),
    foreign key(charID) references character(charID),
    foreign key(matchID) references match(matchID),
    primary key(matchID, charID)

);

-- this table below will relate all the matches that were played at a specific event. 
create table match_played_at_event (

    matchID char(50),
    eventID char(50),
    foreign key(matchID) references match(matchID),
    foreign key(eventID) references event(eventID),
    primary key(matchID, eventID)


);

create table event (

    eventID char(50), -- randomly generated. 
    eventDate date,
    eventName varchar,
    eventURL varchar, -- the idea here is to have a link to the smash.gg page for the tournament. Might not keep this idea...
    primary key(eventID)

);


create table tournament_set (

    setID char(50) UNIQUE,
    eventID char(50), -- can be used to relate the set to a specific tournament.
    primary key(setID, eventID), 
    foreign key(eventID) references event(eventID)


);

create table match_part_of_set (

    matchID char(50),
    setID char(50), -- randomly generated. 
    foreign key(matchID) references match(matchID),
    foreign key(setID) references tournament_set(setID),
    primary key(matchID, setID)

);
