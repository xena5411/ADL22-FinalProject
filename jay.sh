predFilePath="./outputs/pred_als_unseen_course_addPopCourse.csv"
valFile="./hahow/data/val_unseen.csv"

python train_unseen_course.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/preprocessed/modcourse.csv \
--coursekey course_id \
--outputkey course_id \
--bkey b_course_ids \
--lkey l_course_ids \
--testfile $valFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--rankFilePath ./popular/popularCourseRank.csv \
--model bm25 \
--output $predFilePath \
--factors 32 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--learning_rate 0.02 \
--K 20 \
--K1 1.20 \
--B 0.1 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 800.0 \
--l_weight 700 \
--p_weight 700

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \

# --filter_already_liked_items \
# --thresh 0.2 \
