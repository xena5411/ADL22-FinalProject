import torch
import torch.nn as nn
import torch.nn.functional as F
import json
from sklearn.model_selection import train_test_split

class MF(nn.Module):
    def __init__(self, num_users, num_items, emb_size=100):
        super(MF, self).__init__()
        self.user_emb = nn.Embedding(num_users, emb_size)
        self.item_emb = nn.Embedding(num_items, emb_size)
        # initializing our matrices with a positive number generally will yield better results
        self.user_emb.weight.data.uniform_(0, 0.5)
        self.item_emb.weight.data.uniform_(0, 0.5)
    def forward(self, u, v):
        u = self.user_emb(u)
        v = self.item_emb(v)
        return (u*v).sum(1)  # taking the dot product

model = MF(130567, 728, emb_size=100)

with open("./hahow/preprocessed/usersAndCourses.json") as j:
    train_df = json.loads(j.read())
with open("./hahow/preprocessed/valid.json") as j:
    valid_df = json.loads(j.read())

user_id_to_id={}
id = 0
b_course_ids_to_bid={}
bid = 0
def preprocess(data:list)->dict:
    global id,bid
    target = {"user_id":[],"b_course_ids":[],"score":[]}
    for i in data:
        if i["user_id"] not in user_id_to_id:
          user_id_to_id[i["user_id"]] = id
          id+=1
        for j in i["b_course_ids"]:
          if j not in b_course_ids_to_bid:
            b_course_ids_to_bid[j] = bid
            bid+=1
          target["b_course_ids"].append(b_course_ids_to_bid[j])
          target["user_id"].append(user_id_to_id[i["user_id"]])
          target["score"].append(10.0)
    return target
train_df = preprocess(train_df)
test_df = preprocess(valid_df)

# resetting indices to avoid indexing errors
# train_df = train_df.reset_index(drop=True)
# test_df = valid_df.reset_index(drop=True)

print(train_df["user_id"][:10])
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")
model = model.to(device)

def train_epocs(model, epochs=10, lr=0.01, wd=0.0):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    model.train()
    for i in range(epochs):
        usernames = torch.LongTensor(train_df["user_id"])
        usernames = torch.LongTensor(train_df["user_id"]).to(device)
        game_titles = torch.LongTensor(train_df["b_course_ids"]).to(device)
        ratings = torch.FloatTensor(train_df["score"]).to(device)
        y_hat = model(usernames, game_titles)
        loss = F.mse_loss(y_hat, ratings)
        optimizer.zero_grad()  # reset gradient
        loss.backward()
        optimizer.step()
        print(loss.item())
    test(model)

def test(model):
    model.eval()
    usernames = torch.LongTensor(test_df["user_id"]).to(device)
    game_titles = torch.LongTensor(test_df["b_course_ids"]).to(device)
    ratings = torch.FloatTensor(test_df["score"]).to(device)
    y_hat = model(usernames, game_titles)
    loss = F.mse_loss(y_hat, ratings)
    print("test loss %.3f " % loss.item())

train_epocs(model)