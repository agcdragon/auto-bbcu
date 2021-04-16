import webbrowser
import urllib.request
from bs4 import BeautifulSoup
import re
import html
import datetime
import time
import keyboard
import random 

############################################################################
#                   ENTER YOUR BBCU LINKS AND LUNCH BLOCKS                 #
############################################################################

bbcu_links = {
"Period 1": "https://us.bbcollab.com/invite/3f12576", 
"Period 2": "https://us.bbcollab.com/invite/202d810", 
"Period 3": "https://us.bbcollab.com/invite/f138c20", 
"Period 4": "https://us.bbcollab.com/invite/3044c1e", 
"Period 5": "https://us.bbcollab.com/invite/863aa98", 
"Period 6": "https://us.bbcollab.com/invite/5d1c4ef", 
"Period 7": "https://us.bbcollab.com/invite/6aa32f6",  
}

lunch_blue_day = "A"
lunch_red_day = "A"
#############################################################################

now = datetime.datetime.now()

# scrape ion for schedule
def tj_schedule():
	ion = urllib.request.urlopen("https://ion.tjhsst.edu/").read().decode()
	soup = BeautifulSoup(ion, 'html.parser')

	schedule = soup.find("table")
	a = str(schedule).split('<tr class="schedule-block"')
	times = []
	today840 = now.replace(hour=8, minute=40, second=0, microsecond=0)
	for i in a:
		if i.find("data-block-name") != -1:
			pd = html.unescape(re.search(r'(?<=data-block-name=")[^"]*(?=")', i).group().strip())

			start = re.search(r'(?<=data-block-start=")[^"]*(?=")', i).group()
			shm = start.split(":")
			starttime = today840.replace(hour = int(shm[0]), minute = int(shm[1]))
			if starttime < today840:
				starttime = starttime.replace(hour = int(shm[0])+12)

			end = re.search(r'(?<=data-block-end=")[^"]*(?=")', i).group()
			ehm = end.split(":")
			endtime = today840.replace(hour = int(ehm[0]), minute = int(ehm[1]))
			if endtime < today840:
				endtime = endtime.replace(hour = int(ehm[0])+12)

			# print(pd, starttime, endtime)
			times.append((pd, starttime, endtime))

	return times


def configure_lunch(sch):
	updated_sch = []
	for idx, i in enumerate(sch):
		pd = i[0]
		if "Period 3" in pd:
			if pd == "Period 3 & A Lunch":
				if lunch_blue_day == "B":
					updated_sch.append(("Period 3", sch[idx][1], sch[idx+1][2])) 
			elif pd == "Period 3 & B Lunch":
				if lunch_blue_day == "A":
					updated_sch.append(("Period 3", sch[idx-1][1], sch[idx][2]))
		elif "Period 7" in pd:
			if pd == "Period 7 & A Lunch":
				if lunch_red_day == "B":
					updated_sch.append(("Period 7", sch[idx][1], sch[idx+1][2]))
			elif pd == "Period 7 & B Lunch":
				if lunch_red_day == "A":
					updated_sch.append(("Period 7", sch[idx-1][1], sch[idx][2]))
		else:
			updated_sch.append(i)
	return updated_sch



today_schedule = tj_schedule()
today_schedule = configure_lunch(today_schedule)

ct = 0
while True:
	for i in today_schedule:
		now = datetime.datetime.now()
		if i[1] < now < i[2]:
			try:
				link = bbcu_links[i[0]]
			except:
				continue

			webbrowser.open(link, new=0)
			print("Joining class.")

			class_time = int(i[2].timestamp()-now.timestamp()) + int(random.random()*23+7)
			print(class_time, "seconds until class ends.")
			time.sleep(class_time)

			# might need to change this to whatever the mac equivalent is for closing a tab
			keyboard.press_and_release('ctrl+w') 
			print("Leaving class.")

	print("Waiting until class begins...")

	# checks if there is class every minute
	time.sleep(60)