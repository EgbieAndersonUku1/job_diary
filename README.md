# job_diary

## Web Technology used Flask
## DataBase used Mongodb.
## ORM used pymongo.
## language Python 2.7.


I sometimes work for a company that enables me to travel all over London in order to work with different companies. The location sent to me by bosses Simon and Claire can vary from week to week or month to month e.g Wembley, St JohnWoods, Twickenham, to name but a few. So in order to keep track of my job outgoings I often use Excel to keep track of the different locations that I have worked at or will work out. This includes the pay, the time, the length of the job and various aspect relating to the job. But like everything in life there is a downside and this is no different. This particular downside comes in the form of a huge Excel spreadsheet that is sometimes difficult to navigate especially if I looking for a specific month or a job.

This is my primary reason for creating this web application which enables me to track my outgoings by keeping a record of all the different locations that I have worked. This includes the pay, future jobs, etc. By including a web interface this adds abstraction and encapulsation and allow me to access jobs by their attributes e.g. by title, pay, months while hiding the unecssary details

I have used CDN bootstrap to give it a more polish interface. This also means it needs access to the internet in order to render the graphics the way it was intended. 

One of the reason I created job_diary was because jobtracker was limited and did not protect from various attacks such as Cross Site attack. While job diary uses the flask implementation in order to better enhance security.


## project status: complete.

## Run program

## Terminal 1  python run.py runserver.
## Terminal 2  sudo mongod (this starts the server).

## Finally run 127.0.0.1:5000.
