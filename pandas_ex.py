# Pandas 실습
# 실용 단축키
# a. 소괄호 밖 탈출 & 다음 라인으로 이동 : ctrl + shift + enter
# b. 주석처리 : ctrl + /
# c. Debugging : Break point -> F8
import pandas as pd
import matplotlib.pylab as plt

# 1. series 생성 (리스트, 튜플등을 생성자 인수로 받아 생성 가능)
# 인덱스를 지정 안하면 0부터 시작하는 정수형 인덱스가 자동생성
s = pd.Series([0.0, 3.6, 2.0, 5.8, 4.2, 8.0])  # 리스트로 생성
print(s)

# 2. index 정보 변경
s.index = pd.Index([0.0, 1.2, 1.8, 3.0, 3.6, 4.8])  # 인덱스 변경
s.index.name = 'MY_IDX'  # 인덱스명 생성
print(s)

# 3. Series 명 설정
s.name = 'MY_SERIES'
print(s)

# 4. Series 에 데이터 추가
# 4-1. 배열 방식으로 []을 이용하여 추가
s[5.9] = 5.5
print(s)

# 4-2. 새로운 Series 생성 후 append()로 추가
ser = pd.Series([6.7, 4.2], index=[6.8, 8.0])   # 새로운 Series 생성
s = s.append(ser)   # 기존 Series 에 신규 ser 추가
print(s)

# 5. Data 인덱싱
print(s.index[-1])  # index -> 인덱스 값 구하기

# 2개 모두 인덱스(정수) 순서에 해당하는 값을 구함
print(s.values[-1])  # values -> 인덱스에 대한 값 구하기 (복수 결과값 : 배열)
print(s.values[:])
print(s.iloc[-1])  # iloc -> integer location indexer (복수 결과값 : 시리즈)
print(s.iloc[:])

print(s.loc[8.0])   # loc -> 실제 인덱스 값의로 값 구하기

# 6. Data 삭제
# s = s.drop(8.0)  # append와 마찬가지로 결과를 s에 대입해야 함

print(s.describe())

# 7. 시리즈 맷플롯립으로 출력
plt.title("ELLIOTT_WAVE")
plt.plot(s, 'bs--')
plt.xticks(s.index)
plt.yticks(s.values)
plt.grid(True)
plt.show()

