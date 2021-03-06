import markovify
import random
import time
from lxml import html
import requests
import os

###
# GET TRUMP SPEECHES, BUILD MARKOV MODEL
# Get raw text as string.
with open("speeches.txt") as f:
  trump_text = f.read()
with open("civis-corpus.txt") as f:
  civis_text = f.read()


# Build the models.
trump_model = markovify.Text(trump_text, state_size=3)
civis_model = markovify.Text(civis_text, state_size=3)
combo_model = markovify.combine([trump_model, civis_model], [1, 1.5])

### GET CIVIS EMPLOYEE NAMES
page = requests.get('https://civisanalytics.com/team/')
tree = html.fromstring(page.content)

civis_people = tree.xpath('//div[@class="name-team"]/text()')

### DATE RANGE FOR EMAILS
timeformat = "%m/%d/%Y %H:%M"
starttime = time.mktime(time.strptime("06/16/2015 00:00", timeformat))
endtime = time.mktime(time.strptime("10/28/2016 00:00", timeformat))

###
# LOAD IN THE EMAIL TEMPLATE
# Read in the template file
with open('email-template.tex', 'r') as file :
  template = file.read()

###
# MAKE SOME EMAILS!

cwd = os.getcwd()

for email_number in range(30):
  recipient = random.choice(civis_people)
  split = recipient.split()
  recipient = filter(str.isalnum, (split[0][0] + split[1])).lower() + "@civisanalytics.com"

  sender = "realDonaldTrump@trump.com"

  title = combo_model.make_short_sentence(100, tries=100)
  while random.randint(0,1) == 1:
    title = "Re: " + title

  random_time = starttime + random.random()*(endtime-starttime)
  date = time.strftime(timeformat, time.localtime(random_time))

  body = ""
  for paragraph in range(random.randrange(2, 5, 1)):
    for sentence in range(random.randrange(3,10,1)):
      body += combo_model.make_sentence(tries=100)
      body += " "
    body += "\n\n"

  
  email = template.replace("MAIL-RECIPIENT", recipient)
  email = email.replace("MAIL-SENDER", sender)
  email = email.replace("MAIL-TITLE", title)
  email = email.replace("MAIL-DATE", date)
  email = email.replace("MAIL-BODY", body)

  out_name = cwd+'/tex/email-%d.tex' % email_number
  outfile = open(out_name, 'w')
  outfile.write(email)
  outfile.close()

os.system("latexmk -xelatex -outdir=output tex/*.tex")
os.system("mv output/*.pdf pdfs")
