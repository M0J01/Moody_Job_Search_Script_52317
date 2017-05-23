__author__ = 'Jo'

from getTargetData import get_target_data
from getWebpage import get_webpage
from makeFullLink import make_full_link
from fillIndex import fill_index
from getTitle import get_title
from jobRater import job_rater
from sortIndex import sort_index
import time
from datetime import datetime


#Note, you will need to rename the destination file



    #DEFINE INITIAL CONDITIONS ---------------------------------------------------------------------------------------------
    #Create first web address to visit similar to the form;
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Boston%2C+MA"
    #"http://www.indeed.com/jobs?q=Robotics+Engineer&l=Los+Angeles%2C+CA"
    # ??? You can get this by typing a location/title of a job into indeed.com, and then porting it here

url_part1 = "http://www.indeed.com/jobs?q="     # - Leave Me - The root of initial indeed.com searches
url_part2 = "Robotics+Engineering"              # - Change Me - Part where target job area is defined, with + inbetween multiple words
url_part3 = "&l=Boston%2C+MA"                   # - Change Me - City with +'s inbetween, state with %2C+ before 2 letter abreviation
url_base = url_part1 + url_part2 + url_part3    #first web address


    #DEFINE DIRECTORY to store results in------------------------------------------------------------------------------
currenTime = time.strftime("_%d.%m.%Y_%H.%M.%S")
write_text_page_name = "C:/Users/M0J0/Desktop/Job-Search-Python-5-23-17/Offline-Version-Isachron/JobOffline/Results/" + url_part2 + url_part3 + currenTime + ".txt"
write_text_page = open(write_text_page_name,"w")

    #Define patterns to search for-------------------------------------------------------------------------------------
link_style = '\nhref="(.+?)"'     #Pattern of our links to aggregate on indeed.com
name_style = '<title[^.]*>(.+?)</title>'        #Pattern of the name of a given job (Not Very Accurate)
search_count_style = '<div id="searchCount">Jobs[^.]*of (.+?)</div>'    #Pattern of "Total number of jobs" result=

    #Define KeyWords List-----------------------------------------------------------------------------------------------
keyword_list_master = []        #[[supers],[list]]
keyword_list = []               #[[value1, word1, word2, word3...][value2, word1, word2, word3]]
keyword_list_supers = []        #[[[threshold, points worth],[word1, word2, word3]], [[],[]], [[],[]]...]

    #DEFINE KEY WORDS --------------------------------------------------------------------------------------------------
    # ----- MODIFY THESE VALUES TO FIT YOUR DESIRED JOB ------
keyword_list = [
                                        # Any of these words present in a job listing will add the first element worth of points to a job result
	[1,' c,',' c ', ' c.','c\+\+','python','lua','robot', 'hardware','prototy'],
	[10, 'control', 'electrical engineer', 'matlab', 'servo'],
	[30, 'plc', 'microcontroller'],
	[100, 'lab view', 'labview', 'systems engineer']
]

keyword_list_supers = [                 #2 or more appearances for the words from the first list will award a 1 time bonus 1000 points
                                        #Note, any combination of  words from each super group will count towards threshold\
	[[2,1000], ['Jr','Junior','entry level','new grad']],     #i.e. 1x 'entry level' + 1x 'new grad', or 2x 'entry level', etc
    [[2,-200], ['mechanical engineer ']],
	[[2,-200], ['senior','Sr. ']],          #I am not experienced enough to apply for Sr. level positions.
    [[2, -1000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms ']],
    #[[2, -1000], ['ph.d', 'phd', 'master\'s degree', 'masters degree', 'ms. degree', 'ms degree', ' ms ']], #Comment a line our if you don't want to use it anymore
    [[1,-1000], ['5 years','5+ years', '6 years','6+ years', '7 years','7+ years', '8 years', '8+ years', '9 years','9+ years', '10 years', '10+ years']]

]
keyword_list_master.append(keyword_list_supers)
keyword_list_master.append(keyword_list)

startTime = datetime.now()

#Make our first Web request, and get on first page
urlfile = get_webpage(url_base)     #Make the first client request
search_count = get_target_data(search_count_style, urlfile)     #Grab the total number of job results
num_of_search_count = int(search_count[0])                      #Make search count into an int
print ("There are :", num_of_search_count, " Results for :", url_part2, " jobs in the :", url_part3[2:], " area.") #url_part2 is the position title, url_part3 is the geographic area


#6:29:001100

#-------------------------------------------------------------------------------#
#-----------------------------MAIN WHILE LOOP-----------------------------------#
#-------------------------------------------------------------------------------#


index = []                      #Our initial index to store everything in
urlTail = 0                     #keeps track of how many links we have aggregate
root = "http://indeed.com"      #Root to append link endings to later
url_start = url_base            #We will be modifying url_start later


while urlTail <= num_of_search_count:
    temp_index = []

    urlfile = get_webpage(url_start)
    links = get_target_data(link_style, urlfile)
    full_links = make_full_link(links,root)
    temp_index = fill_index(temp_index, full_links)
#    temp_index = get_title(name_style,temp_index)
#    temp_index = job_rater(temp_index, keyword_list_master)

    for a in temp_index:
        index.append(a)

    print url_start
    urlTail +=10
    url_start = url_base+'&start=' + str(urlTail)


#'''
SearchTime = datetime.now() - startTime
print ("Web Search Time Was : ", SearchTime)
#index = fill_index(index, full_links)
index = get_title(name_style, index)
index = job_rater(index, keyword_list_master)
#'''

index = sort_index(index)

print index[1][3]

for a in index:
    write_text_page.write(str(a[3]) + ','+ str(a[4]) + ' : ' + a[0])	##a[3] is type int, so needs to be forced str())
    write_text_page.write('\n')


SortTime = datetime.now() - SearchTime
print "Total Time Was : ", SortTime
totalTime = datetime.now() - startTime
print "Total Time Was : ", totalTime