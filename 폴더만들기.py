'''
os 라는 모듈 내부에 존재하는 폴더 만들기 명령어
os = 기본으로 내장된 모듈(java, c, js, py, ....)
     파일이나 폴더를 다루는 등 운영체제와 상호작용 할 수 있게 해줌

   mkdir = makeDirectory
os.mkdir("폴더이름") 폴더 하나 생성
   rmdir = removedir
os.rmdir("폴더이름") 비어있는 폴더 삭제
os.makedirs("a/b/c")  a폴더 안에 b폴더 안에 c폴더까지 한번에 생성
debug 파이썬  파일이 실행되지 않으면 ctrl+c
'''

import os
# 1. 폴더관련
# os.mkdir("폴더이름")
# os.rmdir("폴더이름")
# os.makedirs("a/b/c")

# 2. 경로 확인
# os.path.exists("명칭") = 파일/폴더 상관없이 해당 명칭의 존재 여부
# os.path.isfile("명칭") = 파일인지 확인
# os.path.isdir("명칭")  = 폴더인지 확인
# os.listdir("경로")     = 해당 경로의 파일/폴더 목록

def 폴더존재유무():
    if os.path.exists("a"):
        print("이미 존재하는 폴더입니다.")
        print("덮어쓰기 / 이름 새로 생성하기 / 취소")
    else:
        os.makedirs("a/b/c")
        print("폴더 생성을 완료하였니다.")

def 잘못된_폴더_동일명칭_생성():
    폴더이름 = "새 폴더"
    카운트 = 1

    # 폴더가 이미 존재하는 경우, 동일한 명칭이 존재하지 않을 때 까지 반복
    while os.path.exists(폴더이름):
        폴더이름 = f"{폴더이름} ({카운트})"
        카운트 += 1 # 기존 숫자에 +1

    os.mkdir(폴더이름)
    print(f"폴더 생성 완료 : {폴더이름}")

    return 폴더이름
'''
새 폴더
새 폴더 (1)
새 폴더 (1) (2)
새 폴더 (1) (2) (3)
....
이런 식으로 만들어짐
'''

def 폴더_동일명칭_생성():
    기존폴더이름 = "새 폴더"
    폴더이름 = 기존폴더이름
    카운트 = 1

    # 폴더가 이미 존재하는 경우, 동일한 명칭이 존재하지 않을 때 까지 반복
    while os.path.exists(폴더이름):
        폴더이름 = f"{기존폴더이름} ({카운트})"
        카운트 += 1 # 기존 숫자에 +1

    os.mkdir(폴더이름)
    print(f"폴더 생성 완료 : {폴더이름}")

    return 폴더이름

# 폴더_동일명칭_생성()

import shutil

def 새폴더_모두_삭제():
    '''
    현재 디렉토리에서 새 폴더로 시작하는 모든 폴더 삭제
    '''
    현재경로 = os.getcwd() # 현재 작업하는 폴더 전체 확인
    삭제된_폴더_목록=[]
    
    for 항목 in os.listdir(현재경로):
        전체경로 = os.path.join(현재경로, 항목)

        # 폴더이고 새 폴더로 시작하는 경우
        if os.path.isdir(전체경로) and 항목.startswith("새 폴더"):
            try:
                shutil.rmtree(전체경로) # 폴더와 폴더 내에 존재하는 내용물 모두 삭제
                삭제된_폴더_목록.append(항목)
                print(f"삭제 완료 : {항목}")
            except Exception as e:
                print(f"삭제 실패 : {항목} - {e}")

    if 삭제된_폴더_목록:
        print(f"총 {len(삭제된_폴더_목록)} 개 폴더 삭제됨")
    else:
        print("삭제할 폴더가 없습니다.")
    return 삭제된_폴더_목록
    
새폴더_모두_삭제()