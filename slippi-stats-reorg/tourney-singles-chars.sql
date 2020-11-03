create view tourneysingleschars as 
select * from 
(match natural join character_played_in_match natural join character)
where gametype='Singles' 
and stagename in ('BATTLEFIELD', 'FINAL_DESTINATION', 'POKEMON_STADIUM', 'YOSHIS_STORY', 'DREAM_LAND_N64', 'FOUNTAIN_OF_DREAMS')