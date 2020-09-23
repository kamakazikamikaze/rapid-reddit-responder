======================
Rapid Reddit Responder
======================

What's this?
------------

Respond to the latest comment of a specific user. That's all.

How do I set this up?
---------------------

You'll need a supported version of Python (recommend 3.6+) with Pip. I recommend
creating a virtualenv to ensure your system's Python does not interfere with packages.

To install dependencies, run:

    pip install -r requirements.txt

For first-time setup only, run:

    python3 responder.py -g config.ini

This will create a template configuration file. Change the config file contents
to match the target user, the account you want to comment with, and the canned
message response.

In the directory where this script will run, create a file named ``praw.ini``
and copy-paste the following:

    [DEFAULT]
    check_for_updates=False
    
    [<ACCOUNT_NAME>]
    redirect_uri=http://localhost:8080
    user_agent=<SOME STRING HERE>
    client_id=<GET THIS FROM THE REGISTRY PAGE>
    client_secret=<GET THIS FROM THE REGISTRY PAGE>
    username=<ACCOUNT_NAME>
    password=<PASSWORD>

Replace all ``<`` and ``>`` and the words in-between with the actual values. If
you do not know what these values are, see the next section.

Finally, determine how often you will run this. For Linux, you can create a cron
job. For Windows, use Task Scheduler. I would recommend not running any quicker
than every 5 minutes to avoid getting shadowbanned.

How do I get Reddit API access?
-------------------------------

`Register your application <https://www.reddit.com/prefs/apps/>`_.
