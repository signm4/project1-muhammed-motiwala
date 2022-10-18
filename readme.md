    was able to post and develop to: 
   https://delicate-violet-7674.fly.dev/
   
    you can get the code for this through Signm4's GitHub!
        - git clone git@github.com:signm4/project1-muhammed-motiwala.git
        You will need your own API Key, to do so go to TMDB's Developer website and follow instructions to sign up as developer
        MAKE SURE KEY IS NOT SHARED
        this Program expects you to have a API KEY,
        make a file named ".env" and in it have TMDB_API_KEY = "YOUR KEY HERE" 

        To run this on your system, make sure you have imported flask, flask start guide can be found on this github example, https://github.com/fly-apps/python-hellofly-flask#readme 
        
        to start this app in your own computer, make sure app.run() is coded in the main python file

        then run the python file in terminal, the app should open in 127.0.0.1:5000

What are at least 2 technical issues you encountered with your project? How did you fix them?

    taking in a input but then making sure it was a integer,
    to debug it i checked that i am taking in a input, then had to see if it was a integer, i thought i was doing it correctly as what i remember you should be doing int(variable), but apparently you have to do variable = int(variable), found this on stackoverflow

    2.genres_str[i] = (i["name"] + " ")
    TypeError: list indices must be integers or slices, not dict
        I am not able to display all genres, tried to fit them in all one string, but only wants to print one, tried debugging by running only that function, and works if standalone but not if in another function. 
        -- was able to fix by defining a string before and then adding through the for loop. was able to figure this out with help from friend.


b. What are at least 2 known problems (still existing), if any, with your project? (If none, what are two things you would improve about your project if given more time?)

Need to fix how the Background image is not actually in the background 

Error You hit a Fly API error with request ID: 01GFNCSGEV679VK61HQJN0KWFR-dfw
fly.io not deploying

fixed fly.io