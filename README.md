<img src='https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white'> <img src='https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white'> <img src='https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=postgresql&logoColor=white'> <img src='https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white'> <img src='https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white'> <img src='https://img.shields.io/badge/nginx-009639?style=flat-square&logo=nginx&logoColor=white'> <img src='https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white'> <img src='https://img.shields.io/badge/CSS-663399?style=flat-square&logo=css&logoColor=white'>

# Employees App
Space for employees for work with financial reports.
<br><br>
Demo: http://employees.eventfun.ru/.
<br>
### Test users accounts:
| login | password | role |
| ----- | -------- | ---- |
| vmrud | q8N7JQQQ83HxjeG | admin |
| darkis | QHAMhTRPHgJ68yq | manager |
| artkulikov | QHAMhTRPHgJ68yq | manager |
| darkis | QHAMhTRPHgJ68yq | manager |

<br>

## 🛠 Develop Mode

### Install and use
Clone the repo and enter into the root folder
```bash
git clone git@github.com:SivikGosh/test_case_web_dev.git
cd test_case_web_dev/
```

Create an environment
```bash
python3.13 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip3 install .[div]
```

Start
```bash
cd project/
python manage.py migrate
python manage.py createsuperuser  # -> username -> password
python manage.py runserver  # http://localhost:8000
```

### Commands
| command            | description                          |
| ------------------ | ------------------------------------ |
| pre-commit install | Install pre-commit hooks file.       |
| pipdeptree         | Show dependency tree.                |
<!-- |                    |                                      | -->

<br>

<div align="right">

## Author's contact
<a href='https://t.me/sivikgosh' target='_blank'><img src='https://img.shields.io/badge/SivikGosh-white?style=flat-square&logo=Telegram&logoColor=26A5E4'></a>

</div>
