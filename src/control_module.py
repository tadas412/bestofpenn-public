def quality_control(quality_weight,flag_count):
	quality_weight = 1 - (flag_count * 0.1)
	return quality_weight

def aggregation_control(users):
	sum_quality_ratings = 0
	sum_quality_weights = 0

	for user in users:
		sum_quality_ratings += (user['weight'] * user['rating'])
		sum_quality_weights += user['weight']

	average_rating = sum_quality_ratings / sum_quality_weights

	return average_rating
