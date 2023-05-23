# Planttracker
Backend for a web-app for tracking home plants, plant errands with automatic addition of errands. (Django+PostgreSQL+Redis+Docker+reportlab)

How to run
git clone https://github.com/annachul/Planttracker
cd Planttracker

Create virtual environment (optional)

python3 -m venv dtb_venv
source dtb_venv/bin/activate

Install all requirements:

pip install -r requirements.txt

Run migrations to setup PostgreSQL database:

python manage.py migrate

Start redis

redis-cli

Start app

./manage.py runserver
