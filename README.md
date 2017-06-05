# Reddit-Text-Scraper
Downloads the text-based contents of a specified subreddit, then packages them into html file for offline browsing


Dependencies: Python 3, Praw (install on linux with pip3 install praw)

In order to use, you must have an app registered under your reddit account.
Once you have that, open Reddit-Text-Scraper.py and put your credentials in the appropriate variables 
(client_id, client_secret, username, and password)

Command Line Arguments:

  -h, --help: show the help message and exit
  
  -s SUBREDDIT, --subreddit SUBREDDIT: Choose a subreddit to download (required!)
                          
  -st SORT, --sort SORT: Choose whether to download hot, new, or top. If unused, will get new
                        
  -p POSTS, --posts POSTS: Choose how many posts to download, default is unlimited
                        
  -nc, --nocomments: Do not download comments
  
  -ncs, --nocss: Do not add css
  
Note that using only the '-s' argument and no others will result in downloading all posts, starting with new ones, including comments
