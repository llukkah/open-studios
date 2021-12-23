# <h1><div align="center">Open Studios</div></h1>

  
***

 ## <div align="center">Open Studios has gone digital!</div>


  - The concept of Open Studios came from a yearly event in New York where artists of all kinds opened their personal studios for all to enjoy, experience and witness.

- With this sense of community, comradery, and support there was no need to navigate politics and contracts of a gallery or museum for an artist to be showcased.

- The Open Studios team is taking this opportunity to give all artists a platform to share vision and works with the world in a digital platform.

- This is the ideal platform for the independent artist you haven't heard of... *yet*.

---

## <div align="center">Our Development Team</div>

### <div align="center">  <table><tr><th>Llukkah Delos Reyes</th><th>Lee Harvey</th><th>Chris Linton </th><th>Jason Rolle </th></tr><tr><td align="center">[@llukkah](https://www.github.com/llukkah) </td><td align="center">[@VirtDev337](https://github.com/VirtDev337) <td align="center">[@Kwyjib0](https://github.com/Kwyjib0)</td><td align="center">[@JasonRolle1990](https://github.com/JasonRolle1990)</td></tr></table></div>
---
[User Guide](Open_Studios_User_Guide.pdf)
---

<details>
## <div align="center"><summary>Installation/Requirements</summary></div>
Open Studios requires [Python](https://www.python.org/) v3.9+  and [Django](https://www.djangoproject.com/) to run.
***

### To run Open Studios-
### 1. Create a directory where you will run a virtual environment. The files for running the virtual environment will be saved in this directory:
```
mkdir <name-of-your-directory>
cd <name-of-your-directory>
```
### 2. Create a virtual environment:
Inside the root folder of the repository, `<name-of-your-directory>`, run:
```
python -m venv <name-of-your-virtual-environment>
or 
python3 -m venv <name-of-your-virtual-environment>
```
### 3. Run the virtual environment:
##### On Windows:
Windows Powershell users:
```
<name-of-your-directory>\Scripts\activate.bat  
or  
<name-of-your-directory>\Scripts\activate.ps1

```
##### On Unix, Linux or MacOS:
```
source <name-of-your-virtual-environment>/bin/activate
```
### 4. Install Django:
Inside the root folder of the repository, `<name-of-your-directory>`, run:
```
pip install django
```
### 5. Install dependencies:
Inside the root folder of the repository, `<name-of-your-directory>`, run:
```
pip install -r requirements.txt
or 
pip freeze > requirements.txt
```
### 6. Run Open Studios:
Make sure your virtual environment is running, then in the directory containing manage.py, run:
```
python manage.py runserver
```
go to  http://127.0.0.1/8000 to launch the Open Studios app

### 7. To deactivate the virtual environment when done:
```
deactivate
or
<name-of-your-directory>\Scripts\deactivate.bat
or
<name-of-your-directory>\Scripts\deactivate.ps1
```
</details>
***

## <div align="center">MVP</div>

  
- Full CRUD capabilities:
--  create your own art exhibit
--  navigate between featured and upcoming art exhibits
--  update and edit an art exhibit and images of related works
-- delete art exhibits and related images
  
---
  
## <div align="center"> WireFrames </div>

  
#### <div align="center">  [Drawio - User Flow](https://app.diagrams.net/#Hllukkah%2Fopen-studios%2Flh-setup%2Ffinal-project.drawio) </div>

  
<div  align="center"><img  src="Site-Flow.png"/></div>

  
---

  
#### <div align="center">  [Mockflow](https://wireframepro.mockflow.com/editor.jsp?editor=off&publicid=M5fea97433a51863da541ae0647ea35801637193735783&projectid=MiKsijI6Xmb&perm=Owner#/page/D59a2638e5631cf8272eb577cc73fa780) </div>
  

<div  align="center"><img  src="mockflow.png"/></div>

  ---

  
## <div align="center"> ERD Model </div>

  
#### <div align="center">  [Lucid Chart](https://lucid.app/lucidchart/4ed7d47e-ad4a-411d-b2e4-89fc68d5c535/edit?viewport_loc=304%2C109%2C1772%2C974%2C0_0&invitationId=inv_75523d29-9bf8-4ac4-b194-262426e46076) </div>

  

<div  align="center"><img  src="ERD-Flow.png"/></div>

---

## <div align="center"> Post MVP </div>

- Implementation of Accounts and Authentication
- Manual upload of image files instead of using URLs
- More search capabilities
- Enhanced styling including an image carousel and other feature

***



***
## <div align="center">Contributing</div>
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 
All changes will be considered but may not be integrated.

Please make sure to update tests as appropriate.
***
Copyright (c) 12/23/2021 Llukkah Delos Reyes, Lee Harvey, Chris Linton, & Jason Rolle


