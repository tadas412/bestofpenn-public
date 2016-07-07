import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

entityRatingsCountFile = sys.argv[1] # count_entity_ratings.sql
usersFile = sys.argv[2] # select * from users
entityRatingsFile = sys.argv[3] # entity_ratings.sql

# Project success
numRatings = []
with open(entityRatingsCountFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        entityID = row[0]
        currNumRatings = int(row[3])
        numRatings.append(currNumRatings)

plt.hist(numRatings)
plt.title('Distribution of Number of Ratings For Entities')
plt.xlabel('Number of Ratings')
plt.ylabel('Frequency (Number of Entities with Rating Count)')
plt.grid(True)
plt.show()

EMAIL = 'email'
CREDITS = 'credits'
QUAL_WEIGHT = 'quality_weight'
FLAG_COUNT = 'flag_count'

# Incentives
users = {}
with open(usersFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        userID = row[0]
        userInfo = {}
        userInfo[EMAIL] = row[1]
        userInfo[CREDITS] = float(row[3])
        userInfo[QUAL_WEIGHT] = float(row[4])
        userInfo[FLAG_COUNT] = int(row[5])
        users[userID] = userInfo

credits = [vals[CREDITS] for userID, vals in users.iteritems()]
plt.hist(credits)
plt.title('Distribution of User Credit Values')
plt.xlabel('Credit Value')
plt.ylabel('Number of Users with Credit Value')
plt.grid(True)
plt.show()

# Quality control
qualityWeights = [vals[QUAL_WEIGHT] for userID, vals in users.iteritems()]
plt.hist(qualityWeights)
plt.title('Distribution of User Quality Weights')
plt.xlabel('Quality Weight')
plt.ylabel('Number of Users with Quality Weight')
plt.grid(True)
plt.show()


# Aggregation
ENTITY_ID = 'entityID'
LIST_ID = 'listID'
LIST_NAME = 'listName'
NUM_RATINGS = 'numRatings'
AVG_RATING = 'avgRating'
STDDEV = 'stddev'


lists = {}
entities = []
with open(entityRatingsFile, 'r') as data:
    reader = csv.reader(data)
    for row in reader:
        if reader.line_num == 1:
            continue
        listID = int(row[0])
        entity = {}
        entity[LIST_ID] = listID
        entity[LIST_NAME] = row[1]
        entity[ENTITY_ID] = int(row[3])
        entity[NUM_RATINGS] = int(row[4])
        entity[AVG_RATING] = float(row[5])
        entity[STDDEV] = float(row[6])

        if listID in lists:
            lists[listID].append(entity)
        else:
            lists[listID] = [entity]

BRUNCH_ID = 2
BYO_ID = 1
REST_ID = 9

def plotListInfo(entityList):
    entityList = sorted(entityList, key=lambda x:x[AVG_RATING], reverse=True)
    avgVals = [e[AVG_RATING] for e in entityList]
    stdDevs = [e[STDDEV] / 2 for e in entityList]

    plt.bar(xrange(len(entityList)), avgVals, yerr=stdDevs, error_kw=dict(ecolor='gray', lw=2,\
        capsize=5, capthick=2))
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
    plt.show()



plotListInfo(lists[BRUNCH_ID])

# numRatings = {}
# entityRatings = {}
# with open(entityRatingsFile, 'r') as data:
    # reader = csv.reader(data)
    # for row in reader:
        # if reader.line_num == 1:
            # continue
        # entityID = row[0]
        # rating = int(row[1])
        # if entityID in entityRatings:
            # entityRatings[entityID].append(rating)
        # else:
            # entityRatings[entityID] = [rating]

        # if entityID in numRatings:
            # numRatings[entityID] = numRatings[entityID] + 1
        # else:
            # numRatings[entityID] = 1

# AVG_RATING = 'avg_rating'
# STD_DEV = 'stddev'
# STD_DEV_DIFF = 'stddev_diff'
# ID = 'entity_id'
# NUM_RATINGS = 'num_ratings'

# entityRatingAgg = []
# for entityID, ratings in entityRatings.iteritems():
    # vals = {}
    # avgRating = np.mean(ratings)
    # stddev = np.std(ratings)
    # print avgRating, stddev, stddev/2

    # vals[ID] = entityID
    # vals[NUM_RATINGS] = numRatings[entityID]
    # vals[AVG_RATING] = avgRating
    # vals[STD_DEV] = stddev
    # vals[STD_DEV_DIFF] = stddev / 2
    # entityRatingAgg.append(vals)

# numEntities = 10
# entityRatingAgg = sorted(entityRatingAgg, key=lambda x:x[NUM_RATINGS],\
        # reverse=True)[:numEntities]
# entityRatingAgg = sorted(entityRatingAgg, key=lambda x:x[AVG_RATING],\
        # reverse=True)
# xVals = xrange(numEntities)
# yVals = []
# errbars = []
# for vals in entityRatingAgg:
    # yVals.append(vals[AVG_RATING])
    # errbars.append(vals[STD_DEV_DIFF])

# plt.bar(xVals, yVals, yerr=errbars, error_kw=dict(ecolor='gray', lw=2,\
    # capsize=5, capthick=2))
# plt.tick_params(
    # axis='x',          # changes apply to the x-axis
    # which='both',      # both major and minor ticks are affected
    # bottom='off',      # ticks along the bottom edge are off
    # top='off',         # ticks along the top edge are off
    # labelbottom='off') # labels along the bottom edge are off
# plt.show()





