predFilePath="../outputs/pred_popular_unseen_course.csv"
valFile="../hahow/data/test_unseen.csv"

python unseenPredPopularCourse.py \
--predFilePath $predFilePath \
--trainFilePath "../hahow/preprocessed/PosAndNegScore.json" \
--valFilePath $valFile \
--type "course_id" \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \