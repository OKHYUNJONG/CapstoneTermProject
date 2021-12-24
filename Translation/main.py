import PapagoTranslate as pt

# 개발자센터에서 발급받은 Client ID 값들
client_id = []
# 개발자센터에서 발급받은 Client Secret 값들
client_secret = []

#csv_path -> "csv파일 경로", ko_column_name -> "csv파일에서의 원하는 한글열에 키 값"
df = pt.PapagoTranslate(client_id,client_secret,"2english.csv","번역")
eng_df = df.eng2ko()
eng_df.to_csv('2korea.csv', index=False)
