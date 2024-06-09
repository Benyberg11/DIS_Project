TLDR version, on my own (windows) computer, just for the 'Flask way' using a virtual environment, for python or for a more comprehensive
flask guide that may work on your computer, see ![Readme](README.md).


For me following these steps worked like a charm:

cd "yourpath"\Medical_manager_prototype
python -m venv .venv
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.venv\Scripts\activate
pip install -r requirements.txt
Set the database configuration in the init.py file.
psql -d {database} -U {username} -W -f clinic/schema.sql
psql -d {database} -U {username} -W -f clinic/schema_ins.sql
psql -d {database} -U {username} -W -f clinic/schema_upd.sql
flask --app run.py run