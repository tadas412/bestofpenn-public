select L.list_id, L.list_name, E.entity_name, E.entity_id, 
COUNT(R.rating) AS num_ratings, AVG(R.rating) AS avg_rating, STDDEV(R.rating) rating_stddev
from entities E
inner join ratings R
on E.entity_id = R.entity_id
inner join lists L
on E.list_id = L.list_id
group by E.entity_id