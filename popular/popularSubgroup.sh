predFilePath="../outputs/pred_popular_course_to_subgroup.csv"
valFile="../hahow/data/test_unseen.csv"

python popularSubgroup.py \
--predFilePath $predFilePath \
--trainFilePath "../hahow/preprocessed/PosAndNegScore.json" \
--rankFilePath "./popularCourseRank.csv" \
--valFilePath $valFile \
--type "course_id" \
