**Social Network**

**Basic models**:
-User
- Post (always made by a user)
**Basic features:**
- user signup
- user login
- post creation
- post like
- post unlike
For User and Post objects, candidate is free to define attributes as they see fit.
**Requirements:**
- Token authentication (JWT is prefered)
- use Django with any other Django batteries, databases etc.


**install:**

>git clone https://github.com/PrefixEt/SocNetworkDRF.git

>pyvenv venv

>source venv/in/activate

>pip install -r requirement.txt

>python manage.py migrate





**Endpoint List:**

-**User:**

> http://hostname:port/api/v1/user/all/  GET return all users.
 
>http://hostname:port/api/v1/user/create/  POST create new json fields: email, first_name, last_name, password 

>http://hostname:port/api/v1/user/update/ PUT json fields: email, first_name, last_name, password, Need JWT auth

> http://hostname:port/api/v1/user/obtain_token/ - POST autentification user. Return JWT fields: email, password

-**Post:**

>http://hostname:port/api/v1/post/all/

>http://hostname:port/api/v1/post/create/ POST create post. Need JWT auth.

>http://hostname:port/api/v1/post/user/<int:user_id>/ GET return posts concrete user by id. 

>http://hostname:port/api/v1/post/id/<int:post_id>/ GET Return post by id

>http://hostname:port/api/v1/post/id/<int:post_id>/like/ POST/PUT like/un like. Need JWT auth

>http://hostname:port/api/v1/post/id/<int:post_id>/likes_list/
