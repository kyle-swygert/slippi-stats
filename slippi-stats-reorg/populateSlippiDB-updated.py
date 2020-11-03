'''
    Repurposed Slippi File renaming Program to populate Slippi Stats Database

    TODO: change all lines where file is renamed to an insert statement into the database. 


'''

from slippi import *
from os import walk, listdir, rename, path
import psycopg2
import uuid
import unicodedata


SlippiStats = "dbname='SlippiStats' user='postgres' host='localhost' password='admin'"
SlippiTest = "dbname='SlippiTest' user='postgres' host='localhost' password='admin'"

databaseConn = ""

conn = psycopg2.connect(
    "dbname='SlippiStats' user='postgres' host='localhost' password='admin'")
cur = conn.cursor()

numFiles = 0

teamDict = {
    0: "Red",
    1: "Blue",
    2: "Green"
}


def connect_to_database():
    hostname = 'localhost'
    dbname = 'SlippiStats'
    username = 'postgres'
    password = 'admin'

    print("Connecting to the database:")

    try:

        conn = psycopg2.connect(
            "dbname='SlippiStats' user='postgres' host='localhost' password='admin'")

        cur = conn.cursor()

        return True

    except:
        print("Could Not Connect to Database...")
        return False


def didWinGame(slippiGame, playerPort):
    # This function will accept a slippi game object, and a player port int that represents the port of the player that is to be checked for the win condition.

    # NOTE: This function will determine who won the match based on who has more than 0 stocks after the final frame. This means that even if 2 players as a team won, the final player on the screen will be said to have only won the match. 

    lastFrame = slippiGame.frames[-1]


    currPlayerData = lastFrame.ports[playerPort]

    if currPlayerData is None:
        return False

    playerPortPostFrameStocks = currPlayerData.leader.post.stocks

    return playerPortPostFrameStocks > 0



def get_datetime(slippiFileName):
    return slippiFileName.split('_')[-1].split('.')[0]


def insert_data_into_database(slippiFileName):

    conn = psycopg2.connect(
        "dbname='SlippiStats' user='postgres' host='localhost' password='admin'")
    cur = conn.cursor()

    # NOTE: this function will run everytime that a file is to be inserted into the database.

    # TODO: remove date-time generation from all other function for this function to work properly!!!!
    # TODO: TEST THIS FUNCTION!!!! HAS NOT BEEN TESTED AT ALL!!



    try:
        slippiGame = Game(slippiFileName)

        gameType = ""

        tempTime = slippiGame.metadata.date

        #print(f"temptime: {tempTime}")

        if slippiGame.start.is_teams == True:

            gameType = "Teams"

        else:  # could be singles or FFA
            #print('non-teams game')
            curPlayerCount = 0
            for player in slippiGame.start.players:
                if player != None:
                    curPlayerCount += 1

            #print(f'players in game: {curPlayerCount}')
            if curPlayerCount == 2:

                gameType = "Singles"

            else:

                gameType = "FFA"

        # TODO: Get the date and time into a format that is able to be used as the time and date format for postgreSQL in the DB.

        # generate unique string for the match
        matchID = str(uuid.uuid4())

        #print(f"Insert {slippiFileName} into the database.")
        #print(f"insert data: uuid: {matchID}, gametype: {gameType}, stage: {slippiGame.start.stage.__dict__['_name_']}, date: {date}, time: {time}")
        #print(f"stage stuff: {slippiGame.start.stage.__dict__}")

        stageName = str(slippiGame.start.stage.__dict__['_name_'])
        stageID = str(slippiGame.start.stage.__dict__['_value_'])

        fileName = slippiFileName

        matchInsert = f"INSERT INTO match(matchID, stageName, stageID, matchdate, gameType, numofframes, filename) VALUES('{matchID}', '{stageName}', {stageID}, TIMESTAMP '{tempTime}', '{gameType}', {slippiGame.metadata.duration}, '{fileName}');"

        # print(matchInsert)

        try:

            #print("before match insert")

            conn = psycopg2.connect(databaseConn)
            cur = conn.cursor()

            # insert the match data into the database.
            cur.execute(matchInsert)
            conn.commit()

            #print("after match insert")

        except Exception as e:
            print(e)
            print("Insert into match failed...")

        curPort = 0

        for player in slippiGame.start.players:

            if player is not None:

                #print(f"name: {player.character.__dict__['_name_']}, color: {player.costume}, tag: {player.tag}")

                charName = player.character.__dict__['_name_']
                cssID = player.character.__dict__['_value_']

                # create a unique ID for each character that is in the database.
                charID = str(uuid.uuid4())

                # This is always set true for now, i think there is code in here from before to determine the winner of the match.
                didWin = True

                team = ""

                if slippiGame.start.is_teams == True:
                    team = teamDict[player.team]

                convertedTag = unicodedata.normalize('NFKC', player.tag)

                charInsert = f"INSERT INTO character(charName, charID, color, didWin, team, tag, portNum, cssid) VALUES('{charName}', '{charID}', {player.costume}, {didWinGame(slippiGame, curPort)}, '{team}', '{convertedTag}', {curPort}, {cssID});"

                try:
                    #print("before char insert")

                    conn = psycopg2.connect(databaseConn)
                    cur = conn.cursor()

                    cur.execute(charInsert)
                    conn.commit()

                    #print("after char insert")

                except Exception as e:
                    print(e)
                    print("failed to insert into char...")


                try:
                    # inserting into the character_played_in_match table

                    charInMatchInsert = f"INSERT INTO character_played_in_match(matchID, charID) VALUES('{matchID}', '{charID}');"

                    conn = psycopg2.connect(databaseConn)
                    cur = conn.cursor()

                    cur.execute(charInMatchInsert)
                    conn.commit()

                except Exception as e:
                    print(e)
                    print("failed to insert into character_played_in_match")



            curPort += 1

        cur.close()

    except Exception as e:
        print(e)
        print(f'## ERROR IN FILE: {slippiFileName}')

    return


def insert_files_from_folder_into_database(folder):
   
    global numFiles

    #print("Connect to the database using the conn global variable")
    #print("NOT YET IMPLEMENTED!!!!")

    connect_to_database()

    #print('folder that contains all the slippi files: {}'.format(folder))

    # check that the folder exists in the system.
    if path.exists(folder) == False:
        #print(f'{folder} does not exist in the system')
        return

    #print(f'{folder} exists, renaming all files in the folder...')

    for root, dirs, files in walk(folder):
        # root represents the current directory that is being processed
        # dirs represents the sub-directories in the currently processing directory
        # files represents the files inside the root directory

       
        #print(f"Processing Directory {root}: ")

        for curr in files:

            # check if the file ends in .slp
            # check that the game is not a teams or FFA
            # if only a 2 player game, send the SlippiGame file to the insert_data_into_database() function.

            if curr.endswith('.slp') == True:

                currFilePath = path.join(root, curr)

                insert_data_into_database(currFilePath)

                numFiles += 1

                if numFiles % 150 == 0:
                    print(f"***** FILES PROCESSED: {numFiles} *****")

            else:
                print(f'WRONG FORMAT: {curr}')
                


# NOTE: this is where the program starts executing when run as a command line program.
if __name__ == "__main__":

    print("DataBase Population Updated:")


    directory = path.join(path.dirname(path.realpath(__file__)), 'slp')

    print(f"Directory being processed: {directory}")

    # Windows filepath
    # "D:\Project Slippi Replays\All WSU Slippi Replays from Google Drive"

    # Linux filepath for use with WSL
    # /mnt/d/Project Slippi Replays/All WSU Slippi Replays from Google Drive

    # NOTE: Change the value of this boolean variable to connect to either the testing database with a smaller dataset or the main database to be used in the C# app.
    testing = True

    wsl = True

    fullFilePath = ""

    if wsl is True:
        fullFilePath = "/mnt/d/Project Slippi Replays/All WSU Slippi Replays from Google Drive"
    else:
        fullFilePath = "D:\\Project Slippi Replays\\All WSU Slippi Replays from Google Drive"



    databaseConn

    print(f'value of testing: {testing}')

    if testing is True:
 
        print(f'testing db insertion')
        databaseConn = SlippiTest
        #insert_files_from_folder_into_database(directory)
        insert_files_from_folder_into_database(fullFilePath)

    else: # testing is False

        print(f'real db insertion')

        databaseConn = SlippiStats
        insert_files_from_folder_into_database(fullFilePath)

    #print("All files in the directory have been renamed.")
