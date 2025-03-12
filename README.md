- python3 --version  
- python3 -m venv env    //virtual environment
- source env/scripts/activate 
- pip install fastapi uvicorn sqlalchemy psycopg2-binary
- uvicorn main:app --reload

##### Folder Structure

```
.
├── .env
├── readme.md
├── .gitignore
├── main.py
└── src:
    ├── core: config.py, base_class.py, session.py, dependencies.py
    ├── Models: userModel.py, profileModel.py, menuModel.py, mailModel.py...
    ├── Schemas: authSchema.py, mailSchema.py, menuSchemas.py, userSchema.py..
    └── Routes: authRoutes.py, userRoutes.py, manage.py, profileRoutes.py, mailRoutes.py...