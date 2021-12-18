import PapagoTranslate as pt

# 개발자센터에서 발급받은 Client ID 값들
client_id = ["AWr3lGFMAb0mYuiojNuR","nS9q6lMn4OLS4Xg2IVGX","Je2rCAH8TBEkIQ2sSqv1","OJSRScAxxUHZ9_rng0wa","OWhh19AhDxntMlpInnKu","n7UXvnWCav52MrH1Z4ag","EabhkoKRJXAZ19ThIMbw","Es33DAi6cmeR2EWZkz48","7y_yiwn_OcWWMyCescN5","k8tO0ttkCX1_GglF3xFZ"]
# 개발자센터에서 발급받은 Client Secret 값들
client_secret = ["8VlNSXhuWu","SFqysutbNr","Q3_EzWzMEj","Yn4Chf2dRR","x0tbFuiizL","BeBkrtpssR","PIQqEkfzmb","ZDlBVY6J9q","1WZx6F4m02","4G2H5XODm0"]

#csv_path -> "csv파일 경로", ko_column_name -> "csv파일에서의 원하는 한글열에 키 값"
df = pt.PapagoTranslate(client_id,client_secret,"2english.csv","번역")
eng_df = df.eng2ko()
eng_df.to_csv('2korea.csv', index=False)