'''
deploy - 배포
vercel 이라는 웹사이트를 이용해서 개발자가 만든 사이트를 인터넷에 업로드
github로 로그인 한 다음에 website에 업데이트 할 repository 이름을 선택
html/css/js 는 requirements.txt나 vercel.json과 같은 파일이 있어야 함

repository가 website에 업로드 될 때 규칙
1. vercel.json
    - vercel 사이트에서 손쉽게 나의 파일을 업로드 할 때 파일이 어떤 형식으로 작성되어 있는지 규칙 작성
    - flask의 경우 시작점이 app.py이기 때문에 
      builds src           use에서 
            어떤파일    @vercel/사용할언어
            시작하는 파일 이름이 뭐고~ 어떤 언어로 만들어진 파일인가?
      routes 그렇다면 app.py는 어디에 있는가?
    - 주의할점
      api/index.py는 예전에 배포할 때 사용하던 방법
      vercel.json만 있다면 위와 같은 파일 형식은 필요하지 않음.

2. templates 폴더와 static 폴더는 반드시 필요.
    메인 페이지의 html 명칭은 무조건 index.html

3. requirements.txt
    프로젝트를 다른 컴퓨터에 옮기거나 다른 사람과 공유할 때,
    vercel과 같은사이트에서 배포를 대신 진행해달라 할 때
    "이 프로그램을 실행하려면 이런 패키지들이 필요해요" 라고 알려주는 파일
    vercel에서는 requirements.txt를 읽고, 아 이런게 필요하군요 하며
    사이트 내에서 참고하여 배포를 진행

    예를 들어 
    pip install flask
    pip install requests

    이런 식으로 하나하나 설치해야하는 프로젝트가 존재.

    컴퓨터를 구매하여 새로 설치해야 하는 상황

    pip install -r requirements.txt를 해주면
    requirements.txt 내부에 작성되어있는 패키지 = 모듈들이 모두 설치가 됨

requirements라는 파일을 만드는 방법

pip freeze > requirements.txt
우리가 설치한 패키지를 얼려서 > 000.txt 이름.확장자로 보관하겠다. 파일 생성

프로젝트 내 전체 폴더와 코드 상태 확인 > 문서이름.확장자이름
      tree /a /f                    >  project.txt

* 주의할 점.
배포 사이트는 폴더 내 이미지 저장이나, json데이터 추가 안됨.
단순 보기용 사이트
배포사이트에 저장 수정 삭제와 같은 기능을 하고 싶다면
서버(데이터베이스+백엔드)

'''
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json, os, uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'posts.json'
MENU_FILE = 'menus.json'
# os = 컴퓨터 시스템
# os.makedirs
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 초기 메뉴 데이터
default_menus = {
    "korean": {
        "name": "한식",
        "emoji": "🍚",
        "items": ["김치찌개", "된장찌개", "불고기", "비빔밥", "제육볶음", "삼겹살", "갈비탕", "냉면"]
    },
    "chinese": {
        "name": "중식",
        "emoji": "🥟",
        "items": ["짜장면", "짬뽕", "탕수육", "마파두부", "깐풍기", "유산슬", "볶음밥", "꿔바로우"]
    },
    "japanese": {
        "name": "일식",
        "emoji": "🍱",
        "items": ["초밥", "라멘", "돈카츠", "우동", "텐동", "규동", "오코노미야키", "타코야키"]
    },
    "western": {
        "name": "양식",
        "emoji": "🍝",
        "items": ["스테이크", "파스타", "피자", "리조또", "햄버거", "샌드위치", "오믈렛", "그라탕"]
    },
    "salad": {
        "name": "샐러드",
        "emoji": "🥗",
        "items": ["시저샐러드", "그릭샐러드", "코브샐러드", "니코이즈샐러드", "참치샐러드", "연어샐러드"]
    }
}

def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def load_menus():
    if not os.path.exists(MENU_FILE):
        save_menus(default_menus)
        return default_menus
    with open(MENU_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_menus(menus):
    with open(MENU_FILE, 'w', encoding='utf-8') as f:
        json.dump(menus, f, ensure_ascii=False, indent=2)

# 게시판 메인 페이지
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

# 메뉴 추천 페이지
@app.route('/menu')
def menu():
    menus = load_menus()
    return render_template('menu.html', menus=menus)

# 메뉴 추가
@app.route('/add_menu', methods=['POST'])
def add_menu():
    category = request.form['category']
    menu_item = request.form['menu_item']
    
    menus = load_menus()
    if category in menus:
        menus[category]['items'].append(menu_item)
        save_menus(menus)
    
    return redirect(url_for('menu'))

# 메뉴 삭제
@app.route('/delete_menu', methods=['POST'])
def delete_menu():
    category = request.form['category']
    menu_item = request.form['menu_item']
    
    menus = load_menus()
    if category in menus and menu_item in menus[category]['items']:
        menus[category]['items'].remove(menu_item)
        save_menus(menus)
    
    return redirect(url_for('menu'))

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        posts = load_posts()

        image_filename = None
        image = request.files.get('image')
        if image and image.filename:
            ext = os.path.splitext(image.filename)[1]
            image_filename = f"{uuid.uuid4()}{ext}"
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))

        post = {
            "id": str(uuid.uuid4()),
            "title": request.form['title'],
            "content": request.form['content'],
            "image": image_filename,
            "created_at": datetime.now().strftime('%Y-%m-%d')
        }

        posts.insert(0, post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('write.html')

@app.route('/view/<post_id>')
def view(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    return render_template('view.html', post=post)

@app.route('/edit/<post_id>', methods=['GET', 'POST'])
def edit(post_id):
    posts = load_posts()
    post = next(p for p in posts if p['id'] == post_id)

    if request.method == 'POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        image = request.files.get('image')
        if image and image.filename:
            ext = os.path.splitext(image.filename)[1]
            image_filename = f"{uuid.uuid4()}{ext}"
            image.save(os.path.join(UPLOAD_FOLDER, image_filename))
            post['image'] = image_filename

        save_posts(posts)
        return redirect(url_for('view', post_id=post_id))

    return render_template('edit.html', post=post)

@app.route('/delete/<post_id>')
def delete(post_id):
    posts = load_posts()
    posts = [p for p in posts if p['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)