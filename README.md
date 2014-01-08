# cmdliner Readme #

## the concept ##
I'd like to provide a REST-ful interface to some CLI-based commands because I'd rather not have to actually have a service require me to log into the machine to restart it.  So my idea was to give CLI-based commands an interface that would tie into a common authentication system, whatever that may be...  I'd have "trusted shell commands" - no ad-hoc stuff around here - and there would be an interface that would 1) permit itself to be discoverable and 2) permit itself to execute and provide the same level of responsiveness as if you were on the console... but, you know, json-ified.   That means output from the command will be viewable, in a tolerable fashion, and you'll get an exit code. 

While the intention is good, I'm not quite sure how functional or acceptable this type of service would be.  I can see it running on an application server and used by a load balancer's health check or used to recover a service should a health check fail.  I can also see it being used as an interface to provide some sort of simple mechanism to execute useful commands for a service that is API-driven, or a CLI-wrapper of sorts for RESTy shops.  

Why not have every linux command wrapped in REST interface!???!?!?!??... (insert bone crushing noises as every sysadmin in the world cringes, especially those who aren't willing to accept the future.... (i digress))

## Running ##

### Server ###
~~~
$ python cmdliner_json.py 
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
~~~

### Client ###
~~~
$ curl  http://localhost:5000/v1.0/cmds
{
  "cmds": [
    {
      "command": "w", 
      "description": "the w command", 
      "id": 1
    }, 
    {
      "command": "top -l1 -u", 
      "description": "the top command", 
      "id": 2
    }
  ]
}

# NOTE THE METHOD HERE...
$ curl -X POST  http://localhost:5000/v1.0/cmds
{
  "message": "405: Method Not Allowed"
}
# ^^^ HERDERRRRR!! DON'T POST DUDE.

# Execute command 1!
$ curl -X POST  http://localhost:5000/v1.0/cmds/1/run
{
  "response": {
    "output": [
      " 1:37  up 3 days, 17:46, 6 users, load averages: 2.76 2.68 2.58", 
      "USER     TTY      FROM              LOGIN@  IDLE WHAT", 
      "user      console  -                21Aug13 139days -", 
      "user      s000     -                14Dec13  1:08 ssh myhawst", 
      "user      s001     -                Tue20       - w", 
      "user      s002     -                Tue21       - curl -X POST http://localhost:5000/v1.0/cmds/1/run", 
      ""
    ], 
    "return_code": 0
  }
}

~~~

## The Files (Yes, they are monolithic) ##

### cmdliner.py ###
this is a BROKE-AZZ flask-based, sqlite3-backed implementation of the cmdliner concept.  It's not functional.  Don't use it.   I heard it carries the flu and H1N1 combined and will transmit at will.  It is bad news in it's current state!

### cmdliner_json.py ###
This is a pure json implementation of the cmdliner

