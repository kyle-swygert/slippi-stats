
-- select all distinct character names that are in the database. 
select distinct(charname) from character order by charname asc;

-- stage winrate
-- selects stagename, number of times played, and winrate for character on said stage from singles tournament matches. 
select stagename, count(*), (sum( case when didwin=true then 1 else 0 end )::float /  count(*)::float) * 100 as winrates
from tourneysingleschars
where charname='charNamePlaceholder'
group by stagename;

-- tag usage
-- selects the tag and number of times the tag is used. 
-- orders from most used to least used. 
select tag, count(*) as uses
from tourneysingleschars
where charname='charNamePlaceholder'
group by tag
order by uses desc;

-- color usage
-- selects the color used and number of times the color is used. (colors are enumerations rather than strings.)
-- orders from most used to least used. 
select color, count(*) as uses
from tourneysingleschars
where charname='charNamePlaceholder'
group by color
order by uses desc;

-- selected character winrate and pickrate
-- selects character name, total number of matches that the charcater played in, calculates the winrate of the selected character, and calculates the pickrate of the selected character. 
select charname, count(*) as totalgames, sum( case when didwin=true then 1 else 0 end)::float / count(*) * 100 as winrate, (select sum( case when charname='charNamePlaceholder' then 1 else 0 end)::float / count(*)::float * 100 as pickrate
from tourneysingleschars)
from tourneysingleschars
where charname = 'charNamePlaceholder'
group by charname;


-- selected character's winrate against all other character in database. 
-- query calculates winrate of selected character against all other characters that are in the database. 
select charname, count(*) as gamesPlayed,
sum(case when didwin=false then 1 else 0 end) * 100 / count(*)::float as winrate
from
(select * from
(select matchid from
(select distinct(matchid) from tourneysingleschars
where charname = 'charNamePlaceholder') matchcontainsselected natural join tourneysingleschars
group by matchid
having count(distinct(didwin))=2) completedmatches
natural join tourneysingleschars
where charname <> 'charNamePlaceholder') opponentchars
group by charname
order by winrate desc;