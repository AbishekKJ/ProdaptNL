# ProdaptNL Assignment - User Feeds

User Feeds is project where we have two services. One service where users write posts
and other one where users comments on posts. These details can be accessed using the external apis

# External apis:
* https://jsonplaceholder.typicode.com/posts
* https://jsonplaceholder.typicode.com/comments

# Task:

Fetch all the posts and comments, store them, and present them in a **single** structure 

# Tech stacks used:


Languages/Frameworks| Version |
--- | --- | 
Python | 3.8 |
Serverless | 2.43.1
AWS Lambda| Python runtime
MongoDB | 4.4.5

# Solution:

**Storing in a Single Structure**

* Approach Followed:
    * Fetched all details from external apis using Python **requests** module
    * Parsed the response json and stored them in **single structure**- **posts**
    * **posts** is the primary single dictionary where you will the **post details, post id, commments associated with the posts and userid**. 
    * Also storing **users** and **comments** dictionaries for future enhancements
    * For Persistent storage, all these dictionaries are stored in MongoDB under database **userFeeds** as separate collections
  
# MongoDB's collection screenshots

POSTS:

<p align="center">
  <img src="./img/Posts.png" alt="Size Limit CLI" width="738">
</p>

Single Post data:

<p align="center">
  <img src="./img/post.png" alt="Size Limit CLI" width="738">
</p>

Users:

<p align="center">
  <img src="./img/users.png" alt="Size Limit CLI" width="738">
</p>

Comments:

<p align="center">
  <img src="./img/comments.png" alt="Size Limit CLI" width="738">
</p>

