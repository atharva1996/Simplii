

[![DOI](https://zenodo.org/badge/404911045.svg)](https://zenodo.org/badge/latestdoi/404911045)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://app.travis-ci.com/atharva1996/Simplii.svg?branch=main)](https://app.travis-ci.com/atharva1996/Simplii)
![Code Coverage](https://github.com/prateeksingamsetty/Simplii/blob/main/src/coverage.svg)
![github workflow](https://github.com/prateeksingamsetty/Simplii/actions/workflows/style_checker.yml/badge.svg)
![github workflow](https://github.com/prateeksingamsetty/Simplii/actions/workflows/syntax_checker.yml/badge.svg)
![github workflow](https://github.com/prateeksingamsetty/Simplii/actions/workflows/close_as_a_feature.yml/badge.svg)

## Link to Demonstration Video of the Project: 
https://youtu.be/GecaW1x1y8k

# SIMPLII 4.0

<h3>Are you trying to manage tasks? Simplii keep track of them, with all new Simplii 4.0!!! </h3>

Introducing Simplii, the almost perfect task management solution. It is similar to having a personal assistant, just like Tony Stark's Jarvis minus its witty quips. Without magic spells or secret societies, Simplii is your go-to partner in task management when it comes to productivity and organization. With Simplii, organizing your to-do list is as effortless as James Bond's flawless style, without the high-speed chases or secret spy devices. If you are prepared to transform an average day into an exceptional day, with the power of the God of Thunder, Thor, or with the determination of Captain America, Simplii let Simplii be your guide to the path of productivity.

<p align="center">
<img width="614"  src="./assets/thor.gif">
</p>


# Table of Contents  

- [Why Simplii?](#why-use-simplii)
- [Implementation](#implementation)
- [Built with:](#built-with)
- [Core Functionalities of the Application:](#core-functionalities-of-the-application)
  - [Register](#register)
  - [Login](#login)
  - [Adding tasks](#adding-tasks)
  - [Task Recommendation and Display](#task-recommendation-and-display)
  - [Modifying tasks Updating and Deleting](#modifying-tasks-updating-and-deleting)
- [Steps for Execution:](#steps-for-execution)
- [Source Code](#source-code)
- [Delta](#delta)
- [Future Scope](#future-scope)
- [Team Members](#team-members)
- [Contribution](#contribution)
- [License](#license)

## Why Simplii?

-Simplii has a user-friendly UI, equally appealing to people of all ages and also people learning to use technology.
-Multi-User Login
-User can add new tasks based on their category.<br>
-Users can update tasks as and when they work on them.<br>
-User can keep track of not just work that is in progress, but also completed tasks.<br>
-Tasks can be viewed based on the priority of the deadline.<br>
-Users can set up email reminders when a task approaches a deadline.<br>
-Most importantly, with simplii, users are always up for a stress-free outing!!!

<p align="center">
<img width="614"  src="./assets/friends-hangout.gif">
</p>



## Implementation:
The video below describes the previous version of Simplii

https://user-images.githubusercontent.com/89509351/144701576-5f2d6677-a741-4d58-b1fe-9a2b012f2b8e.mp4

As you walk through this old version of Simplii, you can observe many errors. Firstly, when the user adds a task, it gets displayed 3 times on the dashboard. Moreover, when the user tries to delete the task, all the tasks in the dashboard get deleted instead of just deleting that single task

In the new version of Simplii, we have resolved all these bugs and added new functionalities.

 
 



## Built with:
<table border = "0px">
  <tr>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" height="40" /><b>Python</b></td>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="40" height="40" /><b>JavaScript</b></td>
<td align="center"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="40" height="40"/><b>HTML5</b></td>
<td align="center"><img src ="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="40" height="40"/><b>CSS3</b></td>
<td align="center"><img src ="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="40" height="40"/><b>Bootstrap</b></td>
<td align="center"><img src ="https://raw.githubusercontent.com/devicons/devicon/v2.14.0/icons/flask/flask-original.svg" width="40" height="40"/><b>Flask</b></td>
<td align="center"><img src ="https://raw.githubusercontent.com/devicons/devicon/v2.14.0/icons/mongodb/mongodb-original.svg" width="40" height="40"/><b>MongoDB</b></td>  
  </tr>
</table>


## Core Functionalities of the Application:
 
 ## Register:
 

https://user-images.githubusercontent.com/89509351/144703691-aa8a10cd-db81-48f9-bc21-467f82a53378.mp4


 
 ## Login:
 https://user-images.githubusercontent.com/89509351/144703694-09252613-a2f7-4dff-a574-b4a20cb69fd4.mp4
 
 ## Adding Tasks:
 

https://user-images.githubusercontent.com/89509351/144703705-0628f2a2-8004-442c-8612-a5de40de92be.mp4


 
 ## Task Recommendation and Display:
 
 

https://user-images.githubusercontent.com/89509351/144703718-a2f478e3-b4ea-4fa2-a784-9a3b5c335a57.mp4
 
 
 ## Modifying the tasks - Updating and Deleting:
 

https://user-images.githubusercontent.com/89509351/144703727-e757e3e4-3776-470f-b08f-516593cb861e.mp4




## Steps for execution
 
 Step 1:
 Install MongoDB using the following link:
 
 https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows
 
 Step 2: 
  Git Clone the Repository 
  
    git clone https://github.com/prateeksingamsetty/Simplii.git
    
  (OR) Download the .zip file on your local machine
  
    https://github.com/prateeksingamsetty/Simplii.git
  
 Step 3:
   Install the required packages by running the following command in the terminal 
   
    pip install -r requirements.txt
    
 Step 4:
    Run the following command in the terminal
    
    python application.py
    
 Step 5:
    Open the URL in your browser:  
      http://127.0.0.1:5000/
      
## Source Code
  
  Link to the repository:
    https://github.com/prateeksingamsetty/Simplii.git
                                                                                                                                                  
 ## Delta
 
 <b> a) Task Tracking based on the type of work</b>
        <li>The earlier version of Simplii just used to do the simple task of keeping track of different kinds of task. However, there was no functionality to                  differentiate the tasks.
        <li>In our updated version of Simplii, the tasks can be tracked based on their types. 
                For instance, there are two types of tasks- Physical and Intellectual, so the users can easily keep  track of their tasks based on the work                         type.
    
 <b>b) Task modification is now simplified!</b>
        <li>In the previous version of Simplii, the tasks did not have the modification functionality in which the user could update some details of his task.                  Moreover, the delete functionality completely failed. When the user tried to delete one task, all his other tasks would get deleted. Thus, it was                   highly  inefficient.
        <li>In our updated version of Simplii, we have eliminated that bug by adding the modification function where the users can easily update and delete the                 tasks as per their convenience.
    
 <b>c) Status Tab is added so that users can easily keep a progress of their work.</b>
        <li>In the previous version of Simplii, there was no functionality of viewing the status of jobs and then segregating them based on their status.
        <li>In our updated version of Simplii, we have added the status tab on dashboard and also created a drop-down functionality so that the users can view                 tasks and update them by selecting the task category(Physical or Intellectual) and the task status(In progress, Done, Blocked).</b>
        
 <b>d) Task Recommendation functionality </b>
        <li>In the previous version of Simplii, tasks were not recommended to the user and thus, the user was unable to keep a track of his progress.
        <li>In this updated version of Simplii, there is a functionality of task recommendation where tasks will be recommended in an order such that the user can complete each of them in the given time frame. Thus, all the tasks will get managed and user will not have to worry about his schedule.</li>
    
   ## Future Scope
  
  The  following features can be implemented in the future scope of this application:
 
   1. Create a mobile application for the web version of the application.
   2. Make the website view port adaptable - the website should look good on phone, tablet and computer.
   3. Create chatbot for the web portal
   4. Create Alerts when the Task deadline is approaching
   5. Add an emergency schedule and recommend tasks based on the new schedule.
   
   ## Team Members
   
  <ul style="list-style-type:  '- ' ; padding: 0;">
  <li><a href="https://github.com/shiva1239" style="text-decoration: none; color: black;"><b>Shiva Vara Prasad Kandhagatla</b></a></li>
  <li><a href="https://github.com/prateeksingamsetty" style="text-decoration: none; color: black;"><b>Prateek Singamsetty</b></a></li>
  <li><a href="https://github.com/laasya2704" style="text-decoration: none; color: black;"><b>Laasya Choudary Nandamuri </b></a></li>
  <li><a href="https://github.com/jramani" style="text-decoration: none; color: black;"><b>Jayanth Ramanidharan</b></a></li>
</ul>

  ## Contribution
  
  Please refer the CONTRIBUTING.md file for instructions on how to contribute to our repository.

  ## License
  
  This project is licensed under the MIT License.
  
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                                   
  
  


      
 
 
 
 
 
 
 
 
 
 
 
 


