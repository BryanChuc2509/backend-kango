
# Backend - Kan-Go

1. Clone the repository : 
``` 
git clone https://github.com/BryanChuc2509/backend-kango
``` 

2. Create a virtual enviroment :
``` 
cd backend-kango
py -3 -m venv .venv
``` 

3. Activate your virtual enviroment: 
``` 
.venv/Scripts/activate
``` 

4. Install dependences :
``` 
cd app
pip install -r requirements.txt
```
5. Create and change to the new branch (based on main):
```
git checkout -b feature_new_branch
```
6. Work on the new branch and when you're done, add the new changes to the staging area with (Don't use "git add .") :
```
git add modules/new_controller.py 
git add modules/new_service.py
...
```
7. Commit your changes with a description: 
```
git commit -m "description about your changes"
```
8. Push changes to your created branch:
```
git push origin feature_new_branch
```

## Run App
if you are in backend-kango/app
``` 
cd ..
flask --app app.app run
```

# Aditionals Dependences 
! Add your dependences if you need it 
