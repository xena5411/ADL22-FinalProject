predFilePath="./outputs/seen_course.csv"
valFile="./hahow/data/val_seen.csv"

python train_seen_course.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/courses.csv \
--coursekey course_id \
--outputkey course_id \
--bkey b_course_ids \
--lkey l_course_ids \
--testfile $valFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--rankFilePath ./popular/popularCourseRank.csv \
--model bm25 \
--output $predFilePath \
--factors 5 \
--regularization 0.01 \
--alpha 1.0 \
--K 60 \
--K1 1.2 \
--B 0.1 \
--iterations 400 \
--learning_rate 0.02 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 1000.0 \
--l_weight 200 \
--p_weight 700

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \

# --filter_already_liked_items \
# --thresh 0.2 \
