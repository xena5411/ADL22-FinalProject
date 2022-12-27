predFilePath="./outputs/pred_bm25_unseen_course_pred_random.csv"
valFile="./hahow/data/val_unseen.csv"

python unseenPredRandomCourse.py \
--predFilePath $predFilePath \
--trainFilePath "./hahow/preprocessed/PosAndNegScore.json" \
--valFilePath $valFile \
--type "course_id" \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \