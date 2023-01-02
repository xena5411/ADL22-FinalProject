# predFilePath="./outputs/als/pred_test_unseen_course_f64_r001_i200_b10_l2.csv"
predFilePath="./outputs/unseen_course.csv"
valFile="./hahow/data/val_unseen.csv"
# CUDA_VISIBLE_DEVICES=2 
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
--factors 64 \
--regularization 0.01 \
--alpha 1.0 \
--iterations 200 \
--K 40 \
--K1 1.2 \
--B 0.1 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 1000.0 \
--l_weight 200.0 \
--p_weight 700.0 \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \

# --filter_already_liked_items \
# --thresh 0.2 \
