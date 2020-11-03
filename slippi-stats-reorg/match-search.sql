
/* 
query searches for the matches that fit the conditions matched in the GUI.

searches based on:
- characters selected
- dates selected 
- tags selected
- stages selected
- team color selected
- gametype selected

note: the {searchCond} variable will only be encased in a 'where (  ) ' section if there are other search conditions selected at all. otherwise all the matches will be selected. 

note: each of the conditions to search based off of are to be separated by an 'and' to make sure that all the desired matches are actually found!


*/

select matchid, stagename, stageid, matchdate, gametype, numofframes, filename 
from (match natural join character_played_in_match natural join character) 
charinmatch 
{searchCond} 
group by matchid 
order by matchdate;