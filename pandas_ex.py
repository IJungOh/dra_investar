# Pandas 실습 (modified GitHub)
# 실용 단축키
# a. 소괄호 밖 탈출 & 다음 라인으로 이동 : ctrl + shift + enter
# b. 주석처리 : ctrl + /
# c. Debugging : Break point -> F8
import pandas as pd

# 1. series 생성 (리스트, 튜플등을 생성자 인수로 받아 생성 가능)
# 인덱스를 지정 안하면 0부터 시작하는 정수형 인덱스가 자동생성
s = pd.Series([0.0, 3.6, 2.0, 5.8, 4.2, 8.0])  # 리스트로 생성
print(s)

# 2. index 정보 변경
s.index = pd.Index([0.0, 1.2, 1.8, 3.0, 3.6, 4.8])  # 인덱스 변경
s.index.name = 'MY_IDX' # 인덱스명 생성
print(s)

# 3. Series 명 설정
s.name = 'MY_SERIES'
print(s)

