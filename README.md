# project1

## 

## Project status

2023.10.20

수환:

- animate.css cdn적용 challenge 페이지에 임시로 적용해봄 (차후에 논의 후 수정)



2023.10.20

지혜:

- 커서 이미지 생성 및 토글 이미지 생성

- 메인 페이지 그리드 추가 및 임시 게시글 생성

수환:

- 마우스 커서 변경 및 on/off 기능 추가

- 챌린지 색깔 변경

2023.10.19

지혜:

- base/background img 변경(static 파일 이미지 변경)
- base toggle(nav 변경)

수환 :

- 모달기능 완성 및 제작 폼 추가
- challenges에 오늘 날짜를 계산하여 on/off 담당할 is_today 필드 추가

2023.10.18

수환 :

- 라이브러리 추가 (seed)

- pagenation/toggle 기능 추가 (challenges/index.html) 같은 기능 구현시 참고할것

지혜:

- settings/media 경로 추가 및 main.models image 추가

- base.html <div> block </div>- d-flex 삭제 및 main 정렬 변경

- base 상단바 image 추가

- main page 게시판 추가 (가운데 정렬)

2023.10.21

해건 :

- base block css 추가

- static img 파일 추가

- PLAN 게시판 추가

2023.10.24

귀현 :

- 프로필(profile.html), 회원정보변경(update.html), 비밀번호변경(change_password.html) 생성
- 위 html 3개에 맞는 url 생성 및 연결
- 회원정보 CustomUserChangeForm 수정 + 비밀번호 변경 CustomPasswordChangeForm 생성 + 각각 form들의 style 추가 및 수정
- 프로필 가운데 image 파일 안에 image 파일 변경할 수 있도록 변경 (개인프로필 사진 in 우주비행사)

건우 :

- 백준 프로필에서 내가 푼 문제 크롤링 코드 완성
  
- solve.av에서 문제 등급과 분류 크롤링 코드 완성

해건 :

- 회원가입 / 로그인 수정 및 리뉴얼

- PLAN 게시판 좋아요 취소 기능 추가

- PLAN 게시판 텍스트 자동 줄바꿈 및 테이블 레이아웃 고정

2023.10.25

해건 :

- 로그인 에러 메세지 디버깅

건우 :

- 문제 크롤링 완료
  
- 문제테이블(문제번호, 이름, 티어) , 분류테이블(이름, 문제번호(N:M)) fixture 생성

2023.10.27

건우 :

- algorithms에 내가 푼 문제 페이지 완성

- 크롤링한 데이터를 이용하여 내가 푼 문제의 랭크 갯수 분류 갯수 구하는 코드 완성

- 위 통계를 이용하여 그래프 그리는 코드 완성

- 내가 푼 문제에서 user를 request.user에서 프로필의 user로 변경


2023.10.28

건우 :

- 내가 푼 문제 페이지에서 각 분류를 누르면 해당 분류 문제를 모아놓은 백준사이트로 보내도록 수정

- accounts의 user모델에 탬플릿에서 사용할 함수 추가

- base.html의 member1 대신 회원가입한 사람들이 보이도록 수정

- 회원가입 후 백준 크롤링이 안 된 상태라서 회원가입을 하면 1번 크롤링하도록 수정

- problem.json과 problemclass.json을 합친 data.json을 생성
