predFilePath="./outputs/unseen_subgroup.csv"
valFile="./hahow/data/val_unseen_group.csv"
testFile="./hahow/data/val_unseen_group.csv"

CUDA_VISIBLE_DEVICES=3 python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/subgroups.csv \
--coursekey subgroup_id \
--outputkey subgroup \
--bkey b_subgroup_ids \
--lkey l_subgroup_ids \
--testfile $testFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--calculate_training_loss \
--output $predFilePath \
--model bm25 \
--K 20 \
--K1 200 \
--B 0.3 \
--b_weight 10 \
--l_weight 2 \
--random_state 42 \
--N 50 \

# --alpha 1.0 \
# --thresh 0.1 \
# --filter_already_liked_items \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "subgroup" \



