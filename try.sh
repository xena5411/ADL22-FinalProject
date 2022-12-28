predFilePath="./outputs/xena/pred_bm25_K80_B01_unseen_course_addPopCourse.csv"
valFile="./hahow/data/val_unseen.csv"

python train_unseen_course.py \
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
--factors 32 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--learning_rate 0.02 \
--K1 0.75 \
--K 20 \
--B 0.5 \
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
