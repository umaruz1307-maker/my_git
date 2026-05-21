import os
from git import Repo

# 1. Укажите СВОЮ ссылку на созданный пустой репозиторий GitHub
GITHUB_REPO_URL = "https://github.com/umaruz1307-maker/my_git.git"

# Текущая папка, где запустился скрипт
current_dir = os.getcwd()

print("1. Создаем файлы для ДЗ...")
# Создаем .gitignore, который скрывает файл Name_Fail
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write("Name_Fail\n")

# Создаем скрываемый файл Name_Fail
with open("Name_Fail", "w", encoding="utf-8") as f:
    f.write("Этот файл останется только на компьютере")

# Создаем главный файл main.py
with open("main.py", "w", encoding="utf-8") as f:
    f.write("print('Hello World')\n")

print("2. Инициализируем Git...")
# git init
repo = Repo.init(current_dir)

print("3. Добавляем файлы и делаем коммит...")
# git add . (добавит только .gitignore и main.py, так как Name_Fail в игноре)
repo.git.add(all=True)
# git commit -m "..."
repo.index.commit("Initial commit with 3 local files")

print("4. Переименовываем ветку в main...")
# git branch -M main
if "main" not in repo.branches:
    repo.git.branch("-M", "main")

print("5. Привязываем GitHub и отправляем код...")
try:
    # git remote add origin <url>
    origin = repo.create_remote("origin", GITHUB_REPO_URL)
except:
    # Если remote уже существует, получаем его
    origin = repo.remote(name="origin")

# git push -u origin main
origin.push(refspec="main:main", set_upstream=True)

print("\n🎉 Все готово! Проверьте ваш GitHub.")