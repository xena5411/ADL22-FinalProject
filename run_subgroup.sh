predFilePath="./outputs/bm25/pred_val_unseen_subgroup_Kone120_B01_l1.csv"
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
--model bm25 \
--output $predFilePath \
--factors 100 \
--regularization 0.01 \
--alpha 1.0 \
--iterations 100 \
--learning_rate 0.02 \
--K1 120 \
--B 0.1 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10 \
--l_weight 0 \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "subgroup" \

# --thresh 0.1 \
# --filter_already_liked_items \

