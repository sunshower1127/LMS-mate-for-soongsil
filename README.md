# 숭실대 온라인 강의 자동듣기 3학년 2학기 ver (2024.09.21)

Sw Selenium(커스텀 셀레니움)으로 구현함.
좀 더 범용적으로 쓸 수 있게 설계함.

[https://github.com/sunshower1127/Sw-Selenium]

---

아래는 구버전 설명

## 숭실대 온라인 강의 자동 듣기 24년 1학기 ver

`python`의 `selenium` 모듈 사용

`driver.py` 의 `Element` class에서 커스텀해서 사용함

`driver.py`에서 `condition` 함수는 함수 인자로 받은 조건들을 `xpath`의 조건식으로 만들어줌

---

## 구 버전보다 나아진 점

1. 정적 wait인 `time.sleep()`을 전부 동적 wait인 `WebDriverWait`로 대체함
   -> 더 깔끔해진 코드와, 이제 로딩이 얼마나 걸리던 프로그램이 작동됨
2. 기존의 `find_element`마다 붙어있던 `try for문`을 `Element.uncertain`에만 쓰도록 함
3. 복잡한 xpath를 `condition`함수를 통해 간단하게 만들었음
   -> element 접근이 더 쉬워지고, 코드가 더욱 간결하고 시맨틱해짐

---

## 만든 기간

2024-03-04 ~ 2024-03-05

---
