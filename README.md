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

>pip install --upgrade pip

>pip install -r requirement.txt

>python manage.py migrate





**Endpoint List:**

-**User:**
```
GET http://hostname:port/api/v1/user/user_manager return list  all users.

GET http://hostname:port/api/v1/user/user_manager/<user_id> return user data by user id. Required fields: email, first_name, last_name, password, Need JWT auth
 
POST http://hostname:port/api/v1/user/user_manager create new user. Required fields: email, first_name, last_name, password 

PUT http://hostname:port/api/v1/user/user_manager/<user_id> update user data Required fields: email, first_name, last_name, password, Need JWT auth

POST http://hostname:port/api/v1/user/login - autentification user. Return JWT. Required fields: email, password
```


```
-**Post:**

GET http://hostname:port/api/v1/post/post_manager return all posts


POST http://hostname:port/api/v1/post/post_manager  create post. Need JWT auth. Required fields: title, message

GET http://hostname:port/api/v1/post/user_id/<int:user_id>  return posts concrete user by user id. 

GET http://hostname:port/api/v1/post/post_manager/id/<int:post_id>  Return post by id

POST/PUT  http://hostname:port/api/v1/post/post_manager/id/<int:post_id>/likelike/unlike. Need JWT auth

GET http://hostname:port/api/v1/post/post_manager/id/<int:post_id>/likes_list return list of users who likes this post
```