# Calendar

Django + bootstrap_sb_admin2 + fullcalendar
The purpose of this app is to add calendar functionality to a basic admin app.
I have incorporated a fullcalendar into Django using the sb_admin2 template.
You can add, delete, and modify events in the calendar.

## How to SetUp
It's best to install Python projects in a Virtual Environment.
```bash
python3 -m venv env
source env/bin/activate
```

Move directories to the virtual environment
Upgrade your pip!
```bash
python -m pip install --upgrade pip
```

```bash
git clone https://github.com/tikuro69/Calendar.git
```
then

```bash
cd mysite
```
Install requirement.txt
```python
pip install -r requirements.txt #install required packages
python manage.py migrate # run first migration
python manage.py runserver # run the server
```

Then locate http://127.0.0.1:8000

