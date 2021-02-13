import sys
import json
from MovieLens import MovieLens
from surprise import SVD

with open('newUserId.json') as f:
  data = json.load(f)

love = []
recommended = {}
pop = []

resp = {
    "userId": data['userId'],
    "Loved": love,
    "recommended": recommended
}

def BuildAntiTestSetForUser(testSubject, trainset):
    fill = trainset.global_mean

    anti_testset = []
    
    u = trainset.to_inner_uid(str(testSubject))
    
    user_items = set([j for (j, _) in trainset.ur[u]])
    anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                             i in trainset.all_items() if
                             i not in user_items]
    return anti_testset

# Pick an arbitrary test subject
testSubject = data['userId']

ml = MovieLens()

# print("Loading movie ratings...")
data = ml.loadMovieLensLatestSmall()

userRatings = ml.getUserRatings(testSubject)
loved = []
hated = []
for ratings in userRatings:
    if (float(ratings[1]) > 4.0):
        loved.append(ratings)
    if (float(ratings[1]) < 3.0):
        hated.append(ratings)

# print("\nUser ", testSubject, " loved these movies:")
# print('------------------------------')
for ratings in loved:
    love.append(ratings[0])
# print("\n...and didn't like these movies:")
# print('----------------------------------')
# for ratings in hated:
#     hate.append(ratings[0])

# print("\nBuilding recommendation model...")
trainSet = data.build_full_trainset()

algo = SVD()
algo.fit(trainSet)

# print("Computing recommendations...")
testSet = BuildAntiTestSetForUser(testSubject, trainSet)
predictions = algo.test(testSet)

recommendations = []

# print("\nWe recommend:")
# print('-------------------')
for userID, movieID, actualRating, estimatedRating, _ in predictions:
    intMovieID = int(movieID)
    recommendations.append((intMovieID, estimatedRating))

recommendations.sort(key=lambda x: x[1], reverse=True)

for ratings in recommendations[:10]:
    # recommended.append(ratings[0])
    recommended[ratings[0]]=ratings[1]

# print('\n\nPOPULAR ONES...')
# print('-------------------')
# for popu in list(ml.getPopularityRanks())[:10]:
#     pop.append(popu)


print(json.dumps(resp))
sys.stdout.flush()
