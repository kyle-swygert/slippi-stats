
-- select all the unique character names and order them alphabetically for use in a combo box to select the character to search for. 
select distinct(charname) from character order by charname asc;


-- computes the winrates of the 2 characters that were selected in the separate combo boxes on the GUI. 
-- note: the 'having' conditions near the bottom make sure that the match finished (someone won and someone lost the match) and that the game was not a ditto match. 
-- note: uses the tourneysingleschars view
select charname, 
count(*) as totalGames,
sum( case when didwin=true then 1 else 0 end) as wins,
sum( case when didwin = true then 1 else 0 end) * 100 / count(*)::float as winrate

from

(select * from 
(select matchid
from tourneysingleschars
where charname in ('char1Placeholder', 'char2Placeholder') 
group by matchid
having count( distinct( charname)) = 2 and count(distinct(didwin)) = 2) as bothcharmatches
natural join tourneysingleschars) as bothchardata

group by charname;



-- computes the winrate of each selected character on each tournament legal stage. 
-- note: the 'having' conditions near the bottom make sure that the match finished (someone won and someone lost the match) and that the game was not a ditto match. 
-- note: uses the tourneysingleschars view
select charname, stagename, 
count(*) as totalGames,
sum( case when didwin=true then 1 else 0 end) as wins,
sum( case when didwin = true then 1 else 0 end) * 100 / count(*)::float as winrate

from

(select * from 
(select matchid
from tourneysingleschars
where charname in ('char1Placeholder', 'char2Placeholder') 
group by matchid
having count( distinct( charname)) = 2 and count(distinct(didwin)) = 2) as bothcharmatches
natural join tourneysingleschars) as bothchardata

group by charname, stagename

order by stagename;