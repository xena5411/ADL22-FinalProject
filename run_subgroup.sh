predFilePath="./outputs/pred_test_unseen_subgroup.csv"
valFile="./hahow/data/val_unseen_group.csv"

python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/subgroups.csv \
--coursekey subgroup_id \
--outputkey subgroup \
--bkey b_subgroup_ids \
--lkey l_subgroup_ids \
--testfile $valFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--model als \
--output $predFilePath \
--factors 32 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10.0 \
--l_weight 10 \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "subgroup" \

# --thresh 0.1 \
# --filter_already_liked_items \

