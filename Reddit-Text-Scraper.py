#! /usr/bin/python3
import praw, os, sys, datetime, argparse, ast

# Setting up Argparser for commandline arguments
parser = argparse.ArgumentParser(description='Downloads text data from a subreddit of your choice')
parser.add_argument("-s", "--subreddit", help="Choose a subreddit to download", action="store")
parser.add_argument("-st", "--sort", help="Choose whether to download hot, new, or top. If unused, will get new", action="store")
parser.add_argument("-p", "--posts", help="Choose how many posts to download, default is unlimited", action="store")
parser.add_argument("-nc", "--nocomments", help="Do not download comments", action="store_false")
args = parser.parse_args()
getcomments = args.nocomments
numberofposts = args.posts
sortby = args.sort
if numberofposts is not None:
	numberofposts = int(numberofposts)

# Setting Variables
client_id = "vnnDcLEJbrO_Qw"
client_secret = "amkevPDeA9XcoJOHBcPV3QXsy40"
username = "7895278412845613"
password = "peoples1"
subname = args.subreddit
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent='Text Post Archiver', username=username)
postnumber = 0

# Making directory with the title of the selected subreddit
os.makedirs(subname, exist_ok=True)

# Gets a post's submission date and time
def getdate(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)
# Makes a blank html file and writes data to it
postslist = open(subname+' Post Archive.html', "a")
archive = """<html>
<LINK REL=StyleSheet HREF=\""""+subname+'/'"""style.css" TYPE="text/css">
<center><head>Posts from /r/"""+subname+"""</head></center>
<body> <br> <br>\n"""
postslist.write(archive)

# Function for downloading and writing posts and comments
def dothestuff():
	# Makes an html file for the current post and sets the file's name to the post's id
	savepost = open(os.path.join(subname, submission.id+'.html'), "a")

	# Increases the index of posts downloaded by 1. Used to display "Saving Post #___..." in console
	global postnumber
	postnumber+= 1
	print('Saving Post #'+str(postnumber)+': '+submission.title)

	# Setting variable to be added to the submission's html file (The ".replace"s fix some errors that make the browser unable to read certain characters properly)
	if submission.selftext_html is not None:
		post = """<html>
<link rel=StyleSheet href="style.css" type="text/css">
<head></head>
		<body> \n<p>"""+submission.title.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p> <p>"""+submission.selftext_html.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p><br><center>Comments</center><br><br>"""
	else:
		post = """<html>
<link rel=StyleSheet href="style.css" type="text/css">
<head></head>
<body> \n<p>"""+submission.title+"""</p> <p>"""+submission.selftext.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p><br><center>Comments</center><br><br>"""
	# Writing current post's title and content to its html file
	savepost.write(post)
	# Checking whether "-nc" argument was used, downloads comments if not
	if getcomments:
		# Sets comments to sort by top rather than new
		submission.comment_sort = 'top'
		# Gets rid of "More comments" attribute error by not trying to download those comments
		submission.comments.replace_more(limit=0)
		# Gets comments for the current submission
		for comment in submission.comments:
			comment = """<p><b>"""+'['+str(comment.score)+' Points] '+str(comment.author)+': '+"""</b>"""+comment.body_html+"""</p> <br>"""
			savepost.write(comment)
	
	# Closes the html tags for the current submission's file
	finish = """ </body> </html>"""
	savepost.write(finish)
	savepost.close()
	# Gets the post's author, score, number of comments, date, and title to be added to the main html file, then adds them
	currentpost = """ <div class="postinfo"> """+str(submission.author)+' ['+str(submission.score)+' points] '+'['+str(submission.num_comments)+' comments] '+str(getdate(submission))+' '+""" <br> <a href=\""""+subname+'/'+submission.id+'.html'+'">'+submission.title.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+'</a> </div> <br>\n\n'""""""
	postslist.write(currentpost)

# Gets and downloads submissions and comments, then adds them to the "Archive" html file in the current directory
if sortby is not None:
	for submission in getattr(reddit.subreddit(subname), sortby)(limit=numberofposts):
		dothestuff()
else:
	for submission in reddit.subreddit(subname).submissions():
		dothestuff()

# Closes the Main html file's tags
finished = """</body> </html>"""
postslist.write(finished)
postslist.close()
cssfile = open(os.path.join(subname, 'style.css'), "a")
csscode = """.md{
	color: #fff;
	background-color: #333;
	padding-left: 10px;
	padding-right: 10px;
	min-height: 10em;
	display: table-cell;
	vertical-align: middle;
	box-shadow: 5px 5px 10px #000;
}
.postinfo{
	color: #fff;
	background-color: #333;
	padding-left: 10px;
	padding-right: 10px;
	min-height: 10em;
	display: table-cell;
	vertical-align: middle;
	box-shadow: 5px 5px 10px #000;
	padding-bottom: 10px;
	padding-top: 5px;
}
body{
background-color: #212121;
color: #fff;
}
A:link {
 color: #add8e6;
 font-weight: bold;
}
A:visited {
 color: #adbce6;
 font-weight: bold;
}
A:hover {
 color: white;
}
"""
cssfile.write(csscode)
cssfile.close()