
CREATE VIEW tourneyteamschars as
SELECT * from 
-- Query to find all match IDs for teams matches that have 4 characters that played in it. These will be all legitimate and full teams games, 2 v 2 matches. 
(select m.*
from 
match as m, character_played_in_match as charinmatch, character as c
where m.matchid = charinmatch.matchid 
and c.charid = charinmatch.charid
and m.gametype='Teams' 
and stagename in ('BATTLEFIELD', 'FINAL_DESTINATION', 'POKEMON_STADIUM', 'YOSHIS_STORY', 'DREAM_LAND_N64', 'FOUNTAIN_OF_DREAMS')
group by m.matchid
having count(*) = 4) as subquery
natural join character_played_in_match NATURAL JOIN character