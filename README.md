# omok-alpha-beta-pruning
알파 베타 프루닝을 사용한 오목

## 프로그램 설명
알파 베타 프루닝을 사용하여 AI vs 인간 또는 AI vs AI 모드 플레이가 가능한 오목입니다.

어떠한 모드든 흑돌이 (AI) 먼저 시작하게 되며 렌주룰은 적용되어 있지 않습니다.

AI의 경우 제한 시간을 두어 연산에 5초 이상이 소요되게 되면 랜덤 위치로 돌을 두게 되고  
인간의 경우 제한 시간이 없습니다.

각 코드의 역할은 다음과 같습니다.

* main.py : 오목을 하기 위해 메인으로 실행해야 할 코드  
코드의 일부를 변경하여 AI vs 인간 또는 AI vs AI 모드 선택 가능
* omok.py : 오목판 상태 및 GUI에 관련된 클래스가 정의되어 있는 코드
* util.py : 편의를 위한 함수가 정의되어 있는 코드
* user_agent.py : 흑돌에 대한 AI 동작이 정의되어 있는 코드
* ai_agent.py : 백돌에 대한 AI 동작이 정의되어 있는 코드

## 사용 방법
### 1. 필요한 패키지 설치
```pip install -r requirements.txt```를 이용하여 필요한 패키지를 설치합니다.

### 2. main.py 수정
HUMAN 변수를 True 또는 False로 지정하여 AI vs 인간 또는 AI vs AI 모드를 결정할 수 있습니다.

```HUMAN = True``` : AI(흑) vs 인간(백)  
```HUMAN = False``` : AI(흑) vs AI(백)

### 3. 프로그램 실행
main.py를 실행하여 오목을 시작합니다.
