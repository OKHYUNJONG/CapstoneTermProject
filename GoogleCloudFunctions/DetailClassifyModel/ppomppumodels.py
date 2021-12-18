import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel,BertTokenizerFast, AlbertModel, BertModel, AutoTokenizer
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from google.cloud import storage
import gcsfs

client = storage.Client()

class CategoryDataset(Dataset):
  def __init__(self, subjects,tokenizer, max_len):
    self.subjects = subjects
    self.tokenizer = tokenizer
    self.max_len = max_len
  def __len__(self):
    return len(self.subjects)
  def __getitem__(self, item):
    subject = str(self.subjects[item])
    encoding = self.tokenizer.encode_plus(
      subject,
      add_special_tokens=True,
      max_length=self.max_len,
      return_token_type_ids=False,
      padding = 'max_length',
      truncation = True,
      return_attention_mask=True,
      return_tensors='pt',
    )
    return {
      'subject_text': subject,
      'input_ids': encoding['input_ids'].flatten(),
      'attention_mask': encoding['attention_mask'].flatten(),
    }
def create_data_loader(df, tokenizer, max_len, batch_size, shuffle_=False, valid=False):
  if valid:
    ds = CategoryDataset(
      subjects=df.title.to_numpy(),
      tokenizer=tokenizer,
      max_len=max_len
      )
  else:
    ds = CategoryDataset(
      subjects=df.title.to_numpy(),
      tokenizer=tokenizer,
      max_len=max_len
    )
  return DataLoader(
    ds,
    batch_size=batch_size,
    num_workers=4,
    shuffle = shuffle_
  )


class ReviewClassifier(nn.Module):
  def __init__(self, n_classes):
    super(ReviewClassifier, self).__init__()
    self.bert = BertModel.from_pretrained("kykim/bert-kor-base")
    self.drop = nn.Dropout(p=0.1)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
    def get_cls(target_size= n_classes):
      return nn.Sequential(
          nn.Linear(self.bert.config.hidden_size, self.bert.config.hidden_size),
          nn.LayerNorm(self.bert.config.hidden_size),
          nn.Dropout(p = 0.1),
          nn.ReLU(),
          nn.Linear(self.bert.config.hidden_size, target_size),
      )  
    self.cls = get_cls(n_classes)
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask,
       return_dict=False
    )
    output = self.drop(pooled_output)
    return self.out(output)

def get_predictions(model, data_loader):
  model = model.eval()
  subject_texts = []
  predictions = []
  prediction_probs = []
  with torch.no_grad():
    for d in data_loader:
      texts = d["subject_text"]
      input_ids = d["input_ids"].to(device)
      attention_mask = d["attention_mask"].to(device)
      outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask
      )
      _, preds = torch.max(outputs, dim=1)
      subject_texts.extend(texts)
      predictions.extend(preds)
      prediction_probs.extend(outputs)
  predictions = torch.stack(predictions).cpu()
  prediction_probs = torch.stack(prediction_probs).cpu()
  return subject_texts, predictions, prediction_probs


def validate(model,data_loader,device,n_examples):
  model = model.eval()
  losses = []
  correct_predictions = 0
  pred = []
  for d in data_loader:
    input_ids = d["input_ids"].to(device)
    attention_mask = d["attention_mask"].to(device)
    outputs = model(
      input_ids=input_ids,
      attention_mask=attention_mask
    )
    _, preds = torch.max(outputs, dim=1)
    pred += preds
  return pred


def digit(df):
  tokenizer_bert_kor_base = BertTokenizerFast.from_pretrained("kykim/bert-kor-base")
  BATCH_SIZE = 16
  MAX_LEN =64

  device = torch.device('cpu')
  model_bert_kor_base = ReviewClassifier(n_classes=32).to(device)
  model_bert_kor_base.bert.encoder.layer = model_bert_kor_base.bert.encoder.layer[0:3]
  model_bert_kor_base.load_state_dict(torch.load('gs://hotmoa-classifymodels/ppomppu_DigitClassfiy.pt',map_location=device))
  model_bert_kor_base.eval()

  data_loader = create_data_loader(df, tokenizer_bert_kor_base, MAX_LEN, BATCH_SIZE, valid=True)

  pred = validate(
    model_bert_kor_base,
    data_loader,
    device,
    len(df)
  )

  for i in range(len(pred)):
    if int(pred[i].item()) == 0:
      pred[i] = '게임'
    elif int(pred[i].item()) == 1:
      pred[i] = '공유기'
    elif int(pred[i].item()) == 2:
      pred[i] = '기타'
    elif int(pred[i].item()) == 3:
      pred[i] = '노트북'
    elif int(pred[i].item()) == 4:
      pred[i] = '데스크탑'
    elif int(pred[i].item()) == 5:
      pred[i] = '마우스'
    elif int(pred[i].item()) == 6:
      pred[i] = '메모리'
    elif int(pred[i].item()) == 7:
      pred[i] = '모니터'
    elif int(pred[i].item()) == 8:
      pred[i] = '보조배터리'
    elif int(pred[i].item()) == 9:
      pred[i] = '블랙박스'
    elif int(pred[i].item()) == 10:
      pred[i] = '선풍기'
    elif int(pred[i].item()) == 11:
      pred[i] = '세탁기'
    elif int(pred[i].item()) == 12:
      pred[i] = '스피커'
    elif int(pred[i].item()) == 13:
      pred[i] = '시계'
    elif int(pred[i].item()) == 14:
      pred[i] = '에어컨'
    elif int(pred[i].item()) == 15:
      pred[i] = '외장하드'
    elif int(pred[i].item()) == 16:
      pred[i] = '이어폰'
    elif int(pred[i].item()) == 17:
      pred[i] = '제습기'
    elif int(pred[i].item()) == 18:
      pred[i] = '청소기'
    elif int(pred[i].item()) == 19:
      pred[i] = '충전기'
    elif int(pred[i].item()) == 20:
      pred[i] = '카메라'
    elif int(pred[i].item()) == 21:
      pred[i] = '케이블'
    elif int(pred[i].item()) == 22:
      pred[i] = '케이스'
    elif int(pred[i].item()) == 23:
      pred[i] = '키보드'
    elif int(pred[i].item()) == 24:
      pred[i] = '태블릿'
    elif int(pred[i].item()) == 25:
      pred[i] = '티비'
    elif int(pred[i].item()) == 26:
      pred[i] = '프린터'
    elif int(pred[i].item()) == 27:
      pred[i] = '핸드폰'
    elif int(pred[i].item()) == 28:
      pred[i] = '헤드폰'
    elif int(pred[i].item()) == 29:
      pred[i] = 'SD카드'
    elif int(pred[i].item()) == 30:
      pred[i] = 'SSD'
    elif int(pred[i].item()) == 31:
      pred[i] = 'VR'

  return pred

