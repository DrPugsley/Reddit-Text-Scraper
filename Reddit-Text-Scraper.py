#! /usr/bin/python3
import praw, os, sys, datetime, argparse, ast

parser = argparse.ArgumentParser(description='Downloads text data from a subreddit of your choice')
parser.add_argument("-s", "--subreddit", help="Choose a subreddit to download", action="store")
parser.add_argument("-st", "--sort", help="Choose whether to download hot, new, or top. If unused, will get new", action="store")
parser.add_argument("-p", "--posts", help="Choose how many posts to download, default is unlimited", action="store")
parser.add_argument("-nc", "--nocomments", help="Do not download comments", action="store_false")
args = parser.parse_args()
getcomments = args.nocomments
numberofposts = args.posts
sortby = args.sort
if not numberofposts is None:
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
<body>\n"""
postslist.write(archive)

# Gets and downloads submissions and comments, then adds them to the "Archive" html file in the current directory
if not sortby is None:
	for submission in getattr(reddit.subreddit(subname), sortby)(limit=numberofposts):
		# Makes an html file for the current post and sets the file's name to the post's id
		savepost = open(os.path.join(subname, submission.id+'.html'), "a")

		# Increases the index of posts downloaded by 1. Used to display "Saving Post #___..." in console
		postnumber+=1
		print('Saving Post #'+str(postnumber)+': '+submission.title.replace("/","."))

		# Setting variable to be added to the submission's html file (The ".replace"s fix some errors that make the browser unable to read certain characters properly)
		if not submission.selftext_html is None:
			post = """<html>
			<head></head>
			<body> \n<p>"""+submission.title+"""</p> <p>"""+submission.selftext_html.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p><br><center>Comments</center><br><br>"""
		else:
			post = """<html>
			<head></head>
			<body> \n<p>"""+submission.title+"""</p> <p>"""+submission.selftext.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p>"""
		savepost.write(post)
		if getcomments:
			# Sets comments to sort by top rather than new
			submission.comment_sort = 'top'
			# Gets rid of "More comments" attribute error by not trying to download those comments
			submission.comments.replace_more(limit=0)
			# Gets comments for the current submission
			for comment in submission.comments:
				comment = """<p><b>"""+'['+str(comment.score)+' Points] '+str(comment.author)+': '+"""</b>"""+comment.body_html+"""</p>"""
				savepost.write(comment)
		# Closes the html tags for the current submission's file
		finish = """ </body> </html>"""
		savepost.write(finish)
		savepost.close()
		# Gets the post's author, score, number of comments, date, and title to be added to the main html file, then adds them
		currentpost = """ """+str(submission.author)+' ['+str(submission.score)+' points] '+'['+str(submission.num_comments)+' comments] '+str(getdate(submission))+' '+"""<a href=\""""+subname+'/'+submission.id+'.html'+'">'+submission.title+'</a> <br>\n\n'""""""
		postslist.write(currentpost)
else:
	for submission in reddit.subreddit(subname).submissions():
		# Makes an html file for the current post and sets the file's name to the post's id
		savepost = open(os.path.join(subname, submission.id+'.html'), "a")

		# Increases the index of posts downloaded by 1. Used to display "Saving Post #___..." in console
		postnumber+=1
		print('Saving Post #'+str(postnumber)+': '+submission.title.replace("/","."))

		# Setting variable to be added to the submission's html file (The ".replace"s fix some errors that make the browser unable to read certain characters properly)
		if not submission.selftext_html is None:
			post = """<html>
			<head></head>
			<body> \n<p>"""+submission.title+"""</p> <p>"""+submission.selftext_html.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p>"""
		else:
			post = """<html>
			<head></head>
			<body> \n<p>"""+submission.title+"""</p> <p>"""+submission.selftext.replace("’","'").replace('”','"').replace("—","--").replace('“','"').replace("‘","'").replace("…","...").replace("–","-")+"""</p>"""
		savepost.write(post)
		if getcomments:
			# Sets comments to sort by top rather than new
			submission.comment_sort = 'top'
			# Gets rid of "More comments" attribute error by not trying to download those comments
			submission.comments.replace_more(limit=0)
			# Gets comments for the current submission
			for comment in submission.comments:
				comment = """<p><b>"""+'['+str(comment.score)+' Points] '+str(comment.author)+': '+"""</b>"""+comment.body_html+"""</p>"""
				savepost.write(comment)
		# Closes the html tags for the current submission's file
		finish = """ </body> </html>"""
		savepost.write(finish)
		savepost.close()
		# Gets the post's author, score, number of comments, date, and title to be added to the main html file, then adds them
		currentpost = """ """+str(submission.author)+' ['+str(submission.score)+' points] '+'['+str(submission.num_comments)+' comments] '+str(getdate(submission))+' '+"""<a href=\""""+subname+'/'+submission.id+'.html'+'">'+submission.title+'</a> <br>\n\n'""""""
		postslist.write(currentpost)

# Closes the Main html file's tags
finished = """</body> </html>"""
postslist.write(finished)
postslist.close()