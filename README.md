# 핫모아 프로젝트(Hotmoa) (Capstone design 2021-2)
* 2019102109 옥현종, 2019102111 유종석

## Overview
#### 과제 선정 배경 및 필요성   
최근 물가 상승으로 인해, 여러 게시판에 사람들끼리 “핫딜”이라는 것 공유하기 시작하였음. 그러나 사람들의 관심사가 제각각이기에, 다양한 종류의 제품들이 게시글로 올라오기 시작하였고, 개개인이 원하는 카테고리의 물품을 찾기가 어려워짐. 또한, 플랫폼 간 핫딜 게시판에 중복된 아이템들이 올라와 검색하는 입장에서 혼동이 있을 수 있음.
#### 과제 주요 내용      
1. 제품 카테고리 세부분류
-> 커뮤니티에서 제공하는 카테고리는 분류가 크게 되어있어 세부적으로 더 분류하여 유저가 원하는 결과를 세부적으로 볼 수 있게 해준다. 크롤링한 데이터를 분석하여 세부분류 기준을 어떻게 정하면 좋을지 생각하고 그 분류기준을 바탕으로 라벨링을 진행한 후 딥러닝 모델을 이용하여 성능을 낸다. 
2. 핫딜 제품 가격 분석 및 추천도 제공
-> 회원의 초기 입력 데이터 (현재는 보유 카드 이용사, 음료와 같은 회원의 관심 물품 분류)를 통해 회원별 추천도 가중치를 주어 반영한다. 예로 물품이 신한카드에서 추가 할인이 있으면 이를 보유한 자의 추천도를 높여준다
-> 현재 여러 쇼핑몰에 동일 제품의 가격을 실시간 크롤링하여 현재 가격이 쇼핑몰에 올라온 가격보다 얼마나 더 싼지 보여준다
3. 뽐뿌, 에펨코리아 등 다수의 플랫폼에 올라오는 같은 내용의 게시글 분류
![image](https://user-images.githubusercontent.com/49023654/146395483-e6cb9f77-1332-4250-b935-adc190904f0b.png)   
위는 동일 제품에 대한 서로 다른 커뮤니티에 유저가 올린 글의 제목이다. 거의 제목이 똑같은 글도 있지만 유사한 글도 있다. 이를 올린 시간 범위, 쇼핑몰, 가격, 제목 등 다양한 요소를 이용하여 동일제품에 대한 글인지 유사도를 검사한다. (완전 정해진 것은 아니지만) 예로 쇼핑몰, 가격 등은 완전 일치하는지 비교를 하고 제목은 벡터화하여 유사도를 높은 threshold를 적용하여 100퍼센트 정확한 동일 제품 다른 글 데이터를 일정량 수집한 후 임의로 몇 개의 데이터는 글을 스위칭하여 동일 제품일 경우 1, 동일 제품이 아닐 경우 0으로 라벨링 한 후 test set, train set, validation set을 잘 나누어 f1-score을 기반으로 여러 가지 모델을 실험하여 최적의 모델을 탐색한다. 생각중인 모델 중 하나는 Bert모델에 제목을 입력하고 나머지 데이터를 정규화 한 후 DNN Classfication을 해주는 모델을 Baseline으로 생각중이다.
4. 관심 있는 제품의 시세 분석 및 비교한 내용 시각화
-> 유저가 편하게 볼 수 있게 1번에 내용인 여러 쇼핑몰 가격 비교 표, 추천도, 과거 가격 데이터 추이 그래프를 시각화 해준다. 
5. 지속적으로 크롤링 할 수 있게 클라우드 서비스를 이용하여 크롤링을 한 후 데이터베이스에 저장해준다.
6. 어플리케이션 혹은 웹으로 개발한다.
7. 크롤링을 한 후 과거 데이터를 EDA하여 다른 유용한 데이터 혹은 방법이 있는지 탐색하고 추가적으로 진행한다. (예로 카테고리 세부분류를 현재 생각중인데 이것이 유의미한 데이터인지 잘 따져보고 진행한다. 만약 유의미하다면 세부분류를 라벨링하여 test set, train set, validation set을 잘 나누어 f1-score을 기반으로 여러 가지 모델을 실험하여 최적의 모델을 탐색한다.
#### 최종결과물의 목표   
1. 동일 제품 중복 게시글의 분류는 중복이라고 인지를 잘못한 경우가 더 치명적이기 때문에 f1-score기반으로 실제로 상용가능한 점수를 목표로 한다. 현재는 0.9 이상을 목표로 하고 있다.
2. 한 눈에 볼 수 있는 UI/UX와 데이터 시각화를 구현한다.
3. 모델API 와 여러 API를 잘 만들어 안정화된 서버를 만든다.
4. 어플리케이션이 완성되면 최대한 많은 홍보를 하여 추천도에 대한 피드백을 받을 수 있게 하고 그 유저들로 인해 발생한 데이터를 분석하여 의미 있게 추천시스템을 강화한다.

## Schedule
| Contents |  9월  |  10월 |  11월 |  12월 | 
|----------|-------|-------|-------|-------|
|  뽐뿌, 에펨코리아 핫딜 게시판 크롤링  |   O   |       |       |        |
|  유사도 검사로 중복 물품 제거         |       |    O   |       |       |  
|  물품 카테고리 분류 시스템 모델 구현  |       |    O   |    O   |       | 
|  앱 및 웹 서비스 구현 및 시각화       |       |       |    O   |    O   | 

## Results

### 모델 ( 세부분류 모델 )  

#### 목적
<img width="900" alt="스크린샷 2021-12-18 오후 7 02 14" src="https://user-images.githubusercontent.com/49023718/146637128-fbb5dfd1-ca64-4fec-8f96-f1a833c5d048.png">

<img width="900" alt="스크린샷 2021-12-18 오후 7 02 26" src="https://user-images.githubusercontent.com/49023718/146637133-4a08f38b-e12a-42c6-913a-00d43a39387f.png">
세부분류를 통해 보기 편한 서비스 제공

### Code (경로 Models/DetailClassifyModels )
#### PreProcessing+Model.ipynb

* 디지털 카테고리 32개로 세분화 라벨링 작업  
* Train/Valid 4:1 Split
* Fasttext, Kor-bert-base, Funnel-kor-base, Ko-gpt2 등 여러모델 Baseline작성 및 실험을 통해 BestModel 선정 -> Kor-bert-base  
  
(%)|Fasttext (Ngrams=2, epoch=120, lr=0.1|kor-bert-base(No upsampling) | kor-bert-base(Upsampling)|Funnel-kor-base(Upsampling)|Ko-gpt2(No upsampling)| albert(No upsampling) |
---|---|---|---|---|---|---|
`validate acc` | 0.804 | 0.902 | 0.895 | 0.902 | 0.881 | 0.888 |  
  
* 전처리 및 EDA  : best MAX input length 설정, 특수문자(기호) 제거
  <img width="600" alt="스크린샷 2021-12-17 오후 5 48 11" src="https://user-images.githubusercontent.com/49023718/146637365-66fd2bac-b256-4385-b411-770a2dfae8f9.png">
    
  위와 같은 Text length 분포를 보여 64로 MAX input Length를 설정  
  
```Python
import re
s1 = re.compile('1+1')
s2 = re.compile('역대가')
s3 = re.compile('특가')
s4 = re.compile('모음집')
s5 = re.compile('모음전')
p = re.compile('[\!@#$%\^&\*\(\)\-\=\[\]\{\}\.,/\?~\+\'"|_:;><`┃…]')

def remove_characters(sentence, lower=True):
    sentence = s1.sub(' ', str(sentence))
    sentence = p.sub(' ', sentence) 
    sentence = s1.sub(' ', sentence)
    sentence = s2.sub(' ', sentence)
    sentence = s3.sub(' ', sentence)
    sentence = s4.sub(' ', sentence)
    sentence = s51.sub(' ', sentence)
    sentence = ' '.join(sentence.split())
    if lower:
        sentence = sentence.lower()
    return sentence

train_df['title'] = train_df['title'].map(remove_characters)
train_df.head()
```
특수문자와 성능에 방해가 될거 같은 단어 (모든 라벨에 중복되는 자주 나오는 단어) 제거

 
* Data Augmenatation :  Back-Translation (경로 Translation 참고 ) 를 파파고 api를 활용해 구현, Pseudo Labeling을 통해 Labeling되지 않은 데이터 이용
* Optimizer: Adamw , Loss: CrossEntropyLoss, Schedular: CosineAnnealingWarmupRestarts

하나의 폴드당 Baseline 대비 성능차이   
   
(%)|kor-bert-base(Baseline)| kor-bert-base(Final Model- 1fold) |  
---|---|---|  
`validate acc` | 0.902 | 0.934 |    

* 5-Fold CrossValidation ensemble  

#### DistilBert.ipynb

* Teacher -> kor-bert-base 5-Fold CrossValidation ensemble  ( 12 hidden layers)
* Student -> small kor-bert-base (4 hidden layers)
* Model Size:  Teacher (450MB) -> Student (220 MB)
```Python
# targets = real target, targets2 = kor-bert-base 5-Fold CrossValidation ensemble model predict 
# loss_fn = CrossEntropyLoss
loss = loss_fn(outputs, targets) + loss_fn(outputs, targets2)
```
아쉬운점: 성능은 따로 Test데이터를 라벨링하려고 했는데 시간상 하지못하여 검증은 못함  
-> Train에서는 정확도가 높았고, 일부 Sample로 테스트 했을때 잘 작동

### 모델 ( 유사도모델 ) 
#### 목적
<img width="900" alt="스크린샷 2021-12-18 오후 7 40 03" src="https://user-images.githubusercontent.com/49023718/146638133-6de3b7b2-dcc0-452d-b914-e0c72e7a3bc5.png">

### Code (경로 Models/SimilarityModel )
#### 유사도모델.ipynb
* 제목에 TF-IDF를 분석해 각각의 row마다 가장 유사한 text를 찾기
* 이를 통해 핫딜 판매처 (쿠팡, 11번가 등), 가격 범위 (오차범위 고려하여)를 고려하여 같으면 제거
```Python
import re
sameproduct = []
for j in range(10):
  products = get_recommendations(df_full.loc[j,"title"])
  products.reset_index(inplace=True)
  for i in range(len(products)):
    try :
      if re.sub(r'[^0-9]', '', products.loc[i,"price"]) == "":
        price1 = 0
      else:
        price1 = int(re.sub(r'[^0-9]', '', products.loc[i,"price"]))
      if re.sub(r'[^0-9]', '', df_full.loc[j,"price"]) == "":
        price2 = 0
      else:
        price2 = int(re.sub(r'[^0-9]', '', df_full.loc[j,"price"]))
    except:
      continue
    if products.loc[i,"hotdeal_place"] == df_full.loc[j,"hotdeal_place"] and abs(((price1 - price2) // price2))< 0.05 and :
      sameproduct += [[products.loc[i,"title"],df_full.loc[j,"title"]]]
```

### 백엔드
<img width="1197" alt="스크린샷 2021-12-18 오후 7 50 49" src="https://user-images.githubusercontent.com/49023718/146638373-05c3bc93-93d3-4ec5-85a5-19bf955a112a.png">


### 프론트엔드
React.js를 이용하여 백엔드에서 구현한 api를 이용해 프론트엔드 작성을 통해 실제 애플리케이션을 구현하였음.


#### 로그인
새로운 유저 회원가입, 기존 회원 로그인, 구글 계정으로 로그인 등을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146641593-6e8a2cf6-a93a-448a-ac64-683e02c73fda.png)


#### 홈 화면
어제자로 올라온 핫딜 게시글을 보여주는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146641615-ff548481-1bc1-4e47-bde8-ac0492fc4dcf.png)


#### 관심 카테고리 화면
유저가 설정한 관심 카테고리를 기준으로 유저가 선택하면 해당 카테고리만 필터링하여 보여주는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146641633-a41afcc8-4131-4720-9f24-55447a972c53.png)


#### 디테일 화면
특정 물품에 대한 게시글을 클릭하면 해당 게시글에 대한 세부 정보를 볼 수 있는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146641647-f8aa6aa5-7cd0-475c-aa90-7536c1bef036.png)


#### 프로필 설정
로그아웃 및 관심 카테고리 선택, 저장을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146641656-10074dac-11b1-4308-9bf2-135c7980b350.png)



## Conclusion
### Model Part
* 라벨링 작업에 상당한 시간이 소요
* 라벨링 작업에 한계로 부족한 데이터를 BackTranslation, Pseudo Labeling을 통해 해결
* 위에 2가지 기법을 포함하여 그 밖에 여러가지 실험을 통해 첫 Fasttext Baseline 0.804 -> Final Kor-Bert-Base 0.934 까지 성능 향상
* 다소 큰 모델 사이즈 (450MB)를 Teacher - Student(DistilBert) 기법을 이용해 250MB로 감소시킴
* 유사도 모델을 구현하였으나 검증과 실제 서비스에 적용은 시간관계상 하지못함 ( 일부 Test 샘플로 Test해본결과 동일 글 잘 감지 )

### Backend Part
* GoogleCloudFunction을 통해 게시글을 스크래핑하고 모델에 적용하여 SQL로 보내는 전체 과정을 구현
* SQL을 프론트엔드에게 URL로 전달하기 위해 Flask를 활용한 API Server 구현하고 EC2에 Docker와 Nginx로 배포

### Frontend Part
* Firebase를 이용한 로그인 기능 및 유저 관심 카테고리 데이터베이스 구축
* React를 이용해 Backend 데이터 시각화 및 주요 기능 구현
   
## Reports
* Upload or link (e.g. Google Drive files with share setting)
* Midterm: [Report](Reports/Midterm.pdf)
* Final: [Report](Reports/Final.pdf), [Demo video](Reports/Demo.mkv)
