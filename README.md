# CapstoneTermProject
Hotmoa Team TermProject
# Project title (Capstone design 2021-2)
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
* Main code, table, graph, comparison, ...
* Web link

``` C++
void Example(int x, int y) {
   ...  
   ... // comment
   ...
}
```


### 프론트엔드
React.js를 이용하여 백엔드에서 구현한 api를 이용해 프론트엔드 작성을 통해 실제 애플리케이션을 구현하였음.

#### 로그인
새로운 유저 회원가입, 기존 회원 로그인, 구글 계정으로 로그인 등을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146391898-eb9911a4-d08b-450a-8f54-1803aef12af2.png)

#### 홈 화면
어제자로 올라온 핫딜 게시글을 보여주는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146391930-60735a7b-0058-49a1-8df9-93f3e681755d.png)

#### 관심 카테고리 화면
유저가 설정한 관심 카테고리를 기준으로 유저가 선택하면 해당 카테고리만 필터링하여 보여주는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146392130-55568573-ac48-44ff-927c-72ccf70011ea.png)

#### 디테일 화면
특정 물품에 대한 게시글을 클릭하면 해당 게시글에 대한 세부 정보를 볼 수 있는 화면을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146392310-908da976-0ac1-40ae-aa9b-ae810b4441ae.png)

#### 프로필 설정
로그아웃 및 관심 카테고리 선택, 저장을 구현하였음.
![image](https://user-images.githubusercontent.com/49023654/146392005-76b6b061-c047-4dce-a287-7d95a2f5ee41.png)


## Conclusion
* Summary, contribution, ...

## Reports
* Upload or link (e.g. Google Drive files with share setting)
* Midterm: [Report](Reports/Midterm.pdf)
* Final: [Report](Reports/Final.pdf), [Demo video](Reports/Demo.mp4)
