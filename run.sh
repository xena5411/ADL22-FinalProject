predFilePath="./outputs/als/pred_val_unseen_course_f64_r005_i300_b10_l1.csv"
valFile="./hahow/data/val_unseen.csv"

python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/courses.csv \
--coursekey course_id \
--outputkey course_id \
--bkey b_course_ids \
--lkey l_course_ids \
--testfile $valFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--model als \
--output $predFilePath \
--factors 64 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--K1 120 \
--B 0.1 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10.0 \
--l_weight 1 \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "course_id" \

# --filter_already_liked_items \
# --thresh 0.2 \
