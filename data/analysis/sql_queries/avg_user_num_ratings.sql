select AVG(A.num_ratings)
from (
	select U.user_id, COUNT(R.entity_id) AS num_ratings
	from users U
	inner join ratings R
	on U.user_id = R.user_id
	group by U.user_id
) A