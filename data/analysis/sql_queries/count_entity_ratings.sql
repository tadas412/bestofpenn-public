select E.entity_id, list_id, entity_name, COUNT(R.rating)
from entities E
inner join ratings R
on E.entity_id = R.entity_id
GROUP BY E.entity_id