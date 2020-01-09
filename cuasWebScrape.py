# from twill.commands import *

# #Note: Only works in python2





# def getData():

# 	go('https://iucrclife.chass.ncsu.edu/lifeforms/index.php'); 
# 	#l = follow('C-UAS Texas A&M Planning Mtg');
# 	links = showlinks(); 
# 	#print(links[6]); 
# 	follow(links[6][0])
# 	showlinks();
	

#import urllib2



import re
import mechanize
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

import numpy as np
import matplotlib.pyplot as plt

def getData(refresh=True):
	#page = ur.urlopen('https://iucrclife.chass.ncsu.edu/lifeforms/index.php')

	if(refresh):

		br = mechanize.Browser(); 
		cj = CookieJar(); 
		br.set_cookiejar(cj); 
		br.set_handle_robots(False);
		br.open('https://iucrclife.chass.ncsu.edu/lifeforms/index.php')

		br.follow_link(nr=6); 

		#print(br.geturl())

		br.form = br.forms()[0]; 

		# for f in br.forms():
		# 	if(f.attrs['id'] == 'pass'):
		# 		br.form = f; 
		# 		break; 
		br.form['password'] = 'LIFE_C-UAS'
		br.submit(); 

		#print(br.geturl()); 

		br.open('https://iucrclife.chass.ncsu.edu/lifeforms/user_meeting.php?id=1792&role=pi'); 
		br.open('https://iucrclife.chass.ncsu.edu/lifeforms/view_form.php?id=20859')
		
		formNumber = 20857; 

		allResponse = []; 

		allNums = [20857,20858,20859,20860,20861,20866,20863,20864,20865,20871,20872,20873,20874,20875,20876,20877,20878,20879,20880,20881,20870,20869,20868,20867,20862]

		for num in allNums:
			responses = {'VI':'','I':'','IC':'','NI':'','A':''}
			br.open('https://iucrclife.chass.ncsu.edu/lifeforms/view_form.php?id={}'.format(num)); 
		
			soup = BeautifulSoup(br.response().read(),features='html5lib'); 
			a = soup.find_all('h4')
			#print(str(a[0])[-7:-5]); 
			responses['VI'] = str(a[0])[-7:-5]
			responses['I'] = str(a[1])[-7:-5]; 
			responses['IC'] = str(a[2])[-7:-5]
			responses['NI'] = str(a[3])[-7:-5]; 
			responses['A'] = str(a[4])[-7:-5];

			for key in responses.keys():
				responses[key] = [int(s) for s in responses[key].split() if s.isdigit()][0]

			allResponse.append(responses); 

		
		np.save('responseData.npy',allResponse); 
	else:
		allResponse = np.load('responseData.npy'); 


	legKeys = {"VI": 'Very Interested', 'I':'Interested', 'IC': 'Interested with Changes','NI':'Not Interested','A':'Abstain'}
	sumResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	colKey = {'VI':'g','I':'b','IC':'y','NI':'r','A':'k'}; 
	for r in allResponse:

		for key in r.keys():
			sumResponses[key].append(int(r[key])); 

	keys = sumResponses.keys(); 

	legList = []; 
	for key in keys:
		x = range(0,len(sumResponses[key]));
		z = np.polyfit(x,sumResponses[key],1); 
		p = np.poly1d(z); 
		plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.3); 
		plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
		legList.append(legKeys[key]); 
		legList.append('{} trend'.format(legKeys[key])); 
		#plt.title(key); 
		#plt.pause(2); 

	totalPer = []; 
	for i in range(0,len(sumResponses['VI'])):
		totalPer.append(0); 
		for key in sumResponses.keys():
			totalPer[-1] += sumResponses[key][i]; 

	plt.plot(totalPer,'m',alpha=0.3)
	x = range(0,len(sumResponses['VI']));
	z = np.polyfit(x,totalPer,1); 
	p = np.poly1d(z); 
	plt.plot(x,p(x),'m--');
	legList.append("Total"); 
	legList.append("Total trend");

	plt.title("C-UAS Winter 2019 Response Trends")
	plt.legend(legList);
	plt.xlabel("Project"); 
	plt.ylabel('# Responses')
	plt.show(); 



	perResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	
	#get percentage at each time
	for t in range(0,len(sumResponses['I'])):
		for key in perResponses.keys():
			perResponses[key].append(sumResponses[key][t]/totalPer[t]); 


	#make bar graph
	ind = range(0,len(sumResponses['VI'])); 

	pA = plt.bar(ind,perResponses['A'],color=colKey['A']); 
	pNI = plt.bar(ind,perResponses['NI'],bottom=perResponses['A'],color=colKey['NI']); 
	pIC = plt.bar(ind,perResponses['IC'],bottom=np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['IC']); 
	pI = plt.bar(ind,perResponses['I'],bottom=np.array(perResponses['IC'])+np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['I']); 
	pVI = plt.bar(ind,perResponses['VI'],bottom=np.array(perResponses['I'])+np.array(perResponses['IC'])+np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['VI']); 

	plt.ylabel("Percentage of Responses"); 
	plt.xlabel("Presentation Number"); 
	plt.legend((pVI,pI,pIC,pNI,pA),('Very Interested','Interested','Interested w/changes','Not Interested','Abstain')); 
	plt.show();


def fall2019GetData(refresh=False):
	if(refresh):
		br = mechanize.Browser(); 
		cj = CookieJar(); 
		br.set_cookiejar(cj); 
		br.set_handle_robots(False);
		br.open('https://iucrclife.chass.ncsu.edu/lifeforms/projectpass_input.php?id=1891')
		# br.follow_link(nr=6); 
		# print(br.geturl());
		br.form = br.forms()[0];
		br.form['password'] = 'LIFE_C-UAS'
		br.submit();

		br.open('https://iucrclife.chass.ncsu.edu/lifeforms/user_meeting.php?id=1891&role=pi'); 
		#br.open('https://iucrclife.chass.ncsu.edu/lifeforms/view_form.php?id=222369')
		#print(br.geturl());

		allResponse = []; 

		#allNums = [20857,20858,20859,20860,20861,20866,20863,20864,20865,20871,20872,20873,20874,20875,20876,20877,20878,20879,20880,20881,20870,20869,20868,20867,20862]
		allNums = [22369,22426,22427,22428,22429,22430,22439,22440,22441,22450,22443,22444,22445,22446,22447,22448,22449,22451,22452,22453,22454,22438,22437,22436,22442];

		for num in allNums:
			print("Grabbing Page: {} of {}".format(allNums.index(num)+1,len(allNums))); 

			responses = {'VI':'','I':'','IC':'','NI':'','A':''}
			br.open('https://iucrclife.chass.ncsu.edu/lifeforms/view_form.php?id={}'.format(num)); 
			#print(num);
			#print(br.response().read())

			soup = BeautifulSoup(br.response().read(),features='html5lib'); 
			#print(soup);
			a = soup.find_all('h4')
			#print(a)
			responses['VI'] = str(a[0])[-7:-5]
			responses['I'] = str(a[1])[-7:-5]; 
			responses['IC'] = str(a[2])[-7:-5]
			responses['NI'] = str(a[3])[-7:-5]; 
			responses['A'] = str(a[4])[-7:-5];

			for key in responses.keys():
				responses[key] = [int(s) for s in responses[key].split() if s.isdigit()][0]

			allResponse.append(responses); 

		#print(allResponse)
		print("Codex Acquired, Saving Now..."); 
		np.save('fall2019ResponseData.npy',allResponse); 


def parseData(save=False,file = 'fall2019ResponseData.npy',semester='Fall2019'):
	allResponse = np.load(file); 

	#print(allResponse); 


	#legKeys = {"VI": 'Very Interested', 'I':'Interested', 'IC': 'Interested with Changes','NI':'Not Interested','A':'Abstain'}
	legKeys = {"VI": 'Great Progress', 'I':'On course', 'IC': 'Needs change','NI':'Off course','A':'Abstain'}
	sumResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	colKey = {'VI':'g','I':'b','IC':'y','NI':'r','A':'k'}; 
	for r in allResponse:
		flag = True;
		for key in r.keys():
			if(int(r[key]) != 0):
				flag = False; 
		if(flag):
			continue; 

		for key in r.keys():
			sumResponses[key].append(int(r[key])); 



	keys = sumResponses.keys(); 

	legList = []; 
	for key in keys:
		x = range(0,len(sumResponses[key]));
		z,V = np.polyfit(x,sumResponses[key],1,cov=True); 
		V = np.sqrt(V[1,1]); 
		p = np.poly1d(z); 
		plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
		plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
		#plt.fill_between(x,p(x)+V,p(x)-V,color=colKey[key],alpha=0.2); 
		legList.append(legKeys[key]); 
		legList.append('{} trend'.format(legKeys[key])); 
		#plt.title(key); 
		#plt.pause(2); 

	totalPer = []; 
	for i in range(0,len(sumResponses['VI'])):
		totalPer.append(0); 
		for key in sumResponses.keys():
			totalPer[-1] += sumResponses[key][i]; 

	plt.plot(totalPer,'m',alpha=0.3)
	x = range(0,len(sumResponses['VI']));
	z,V = np.polyfit(x,totalPer,1,cov=True);
	V = np.sqrt(V[1,1]); 
	p = np.poly1d(z); 
	plt.plot(x,p(x),'m--');
	#plt.fill_between(x,p(x)+V,p(x)-V,color='m',alpha=0.2); 
	legList.append("Total"); 
	legList.append("Total trend");

	plt.title("C-UAS {} Response Trends".format(semester))
	plt.legend(legList);
	plt.xlabel("Project"); 
	plt.ylabel('# Responses')
	plt.axvline(8.5,c='k')
	if(save):
		plt.savefig('{}ResponseTrends.png'.format(semester)); 
	else:
		plt.show(); 


def percentagePlots(save=False,file = 'fall2019ResponseData.npy',semester='Fall2019'):
	allResponse = np.load(file); 

	#print(allResponse); 


	#legKeys = {"VI": 'Very Interested', 'I':'Interested', 'IC': 'Interested with Changes','NI':'Not Interested','A':'Abstain'}
	legKeys = {"VI": 'Great Progress', 'I':'On course', 'IC': 'Needs change','NI':'Off course','A':'Abstain'}
	sumResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	colKey = {'VI':'g','I':'b','IC':'y','NI':'r','A':'k'}; 
	for r in allResponse:
		flag = True;
		for key in r.keys():
			if(int(r[key]) != 0):
				flag = False; 
		if(flag):
			continue; 

		for key in r.keys():
			sumResponses[key].append(int(r[key])); 
	totalPer = []; 
	for i in range(0,len(sumResponses['VI'])):
		totalPer.append(0); 
		for key in sumResponses.keys():
			totalPer[-1] += sumResponses[key][i]; 
	perResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	
	#get percentage at each time
	for t in range(0,len(sumResponses['I'])):
		for key in perResponses.keys():
			perResponses[key].append(sumResponses[key][t]/totalPer[t]); 


	#make bar graph
	ind = range(0,len(sumResponses['VI'])); 

	pA = plt.bar(ind,perResponses['A'],color=colKey['A']); 
	pNI = plt.bar(ind,perResponses['NI'],bottom=perResponses['A'],color=colKey['NI']); 
	pIC = plt.bar(ind,perResponses['IC'],bottom=np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['IC']); 
	pI = plt.bar(ind,perResponses['I'],bottom=np.array(perResponses['IC'])+np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['I']); 
	pVI = plt.bar(ind,perResponses['VI'],bottom=np.array(perResponses['I'])+np.array(perResponses['IC'])+np.array(perResponses['NI'])+np.array(perResponses['A']),color=colKey['VI']); 

	plt.ylabel("Percentage of Responses"); 
	plt.xlabel("Presentation Number"); 
	plt.legend((pVI,pI,pIC,pNI,pA),('Great Progress','On Course','Needs Change','Off Course','Abstain')); 
	
	if(save):
		plt.savefig('{}ResponseBars.png'.format(semester)); 
	else:
		plt.show(); 


	plt.figure(); 
	ind = range(0,len(sumResponses['VI'])); 
	for key in colKey.keys():
		plt.plot(ind,perResponses[key],color=colKey[key],label=legKeys[key]); 
		z = np.polyfit(ind,perResponses[key],1,cov=False);
		p = np.poly1d(z); 
		plt.plot(ind,p(ind),color=colKey[key],linestyle='--',linewidth=2); 
	plt.xlabel("Presentation Number"); 
	plt.ylabel("Percentage of Responses"); 
	plt.legend(); 

	if(save):
		plt.savefig('{}ResponsePers.png'.format(semester)); 
	else:
		plt.show(); 

def sessionParse(save=False,file = 'fall2019ResponseData.npy',semester='Fall2019'):
	allResponse = np.load(file); 

	#print(allResponse); 


	#legKeys = {"VI": 'Very Interested', 'I':'Interested', 'IC': 'Interested with Changes','NI':'Not Interested','A':'Abstain'}
	legKeys = {"VI": 'Great Progress', 'I':'On course', 'IC': 'Needs change','NI':'Off course','A':'Abstain'}
	sumResponses = {'VI':[],'I':[],'IC':[],'NI':[],'A':[]}; 
	colKey = {'VI':'g','I':'b','IC':'y','NI':'r','A':'k'}; 
	for r in allResponse:
		flag = True;
		for key in r.keys():
			if(int(r[key]) != 0):
				flag = False; 
		if(flag):
			continue; 

		for key in r.keys():
			sumResponses[key].append(int(r[key])); 

	plt.figure();

	keys = sumResponses.keys(); 

	cuts = [9,17,27]; 
	sigma = 1; 

	legList = []; 
	for key in keys:
		#x = range(0,len(sumResponses[key]));
		x = range(0,cuts[0]); 
		try:
			z,V = np.polyfit(x,sumResponses[key][0:cuts[0]],1,cov=True); 
			V = sigma*np.sqrt(V[1,1]); 
			p = np.poly1d(z); 
			plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
			plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
			plt.fill_between(x,p(x)+V,p(x)-V,color=colKey[key],alpha=0.2); 
		except:
			z = np.polyfit(x,sumResponses[key][0:cuts[0]],1); 
			p = np.poly1d(z); 
			plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
			plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
		legList.append(legKeys[key]); 
		legList.append('{} trend'.format(legKeys[key])); 
		#plt.title(key); 
		#plt.pause(2); 
	

		if(len(sumResponses[key]) > cuts[0]+1):
			#x = range(0,len(sumResponses[key]));
			x = range(cuts[0],cuts[1]); 

			try:
				z,V = np.polyfit(x,sumResponses[key][cuts[0]:cuts[1]],1,cov=True); 
				#V = 2*np.sqrt(V[1,1]); 
				V = sigma*np.std(sumResponses[key][cuts[0]:cuts[1]])
				p = np.poly1d(z); 
				#plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
				plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
				plt.fill_between(x,p(x)+V,p(x)-V,color=colKey[key],alpha=0.2); 
			except:
				z = np.polyfit(x,sumResponses[key][cuts[0]:cuts[1]],1); 
				p = np.poly1d(z); 
				#plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
				plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
				#legList.append(legKeys[key]); 
				#legList.append('{} trend'.format(legKeys[key])); 
		if(len(sumResponses[key]) > cuts[1]+1):

			#x = range(0,len(sumResponses[key]));
			x = range(cuts[1],min(len(sumResponses[key]),cuts[2])); 

			try:
				z,V = np.polyfit(x,sumResponses[key][cuts[1]:min(len(sumResponses[key]),cuts[2])],1,cov=True); 
				#V = 2*np.sqrt(V[1,1]); 
				V = sigma*np.std(sumResponses[key][cuts[1]:min(len(sumResponses[key]),cuts[2])])
				#print(V)
				p = np.poly1d(z); 
				#plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
				plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 
				plt.fill_between(x,p(x)+V,p(x)-V,color=colKey[key],alpha=0.2); 
			except:
				z = np.polyfit(x,sumResponses[key][cuts[1]:min(len(sumResponses[key]),cuts[2])],1); 
				p = np.poly1d(z); 
				#plt.plot(sumResponses[key],c=colKey[key],linewidth = 2,alpha=0.2); 
				plt.plot(x,p(x),'{}--'.format(colKey[key]),linewidth=2); 


	totalPer = []; 
	for i in range(0,len(sumResponses['VI'])):
		totalPer.append(0); 
		for key in sumResponses.keys():
			totalPer[-1] += sumResponses[key][i]; 

	plt.plot(totalPer,'m',alpha=0.3)
	
	# x = range(0,len(sumResponses['VI']));
	# z,V = np.polyfit(x,totalPer,1,cov=True);
	# V = 2*np.sqrt(V[1,1]); 
	# p = np.poly1d(z); 
	# plt.plot(x,p(x),'m--');
	# plt.fill_between(x,p(x)+V,p(x)-V,color='m',alpha=0.2); 
	# legList.append("Total"); 
	# legList.append("Total trend");

	x = range(0,cuts[0]);
	z,V = np.polyfit(x,totalPer[0:cuts[0]],1,cov=True);
	V = sigma*np.sqrt(V[1,1]); 
	p = np.poly1d(z); 
	plt.plot(x,p(x),'m--');
	plt.fill_between(x,p(x)+V,p(x)-V,color='m',alpha=0.2); 
	legList.append("Total"); 
	legList.append("Total trend");
	if(len(sumResponses['VI']) > cuts[0]+1):
		try:
			x = range(cuts[0],cuts[1]);
			z,V = np.polyfit(x,totalPer[cuts[0]:cuts[1]],1,cov=True);
			#V = 2*np.sqrt(V[1,1]); 
			V = sigma*np.std(totalPer[cuts[0]:cuts[1]])
			p = np.poly1d(z); 
			plt.plot(x,p(x),'m--');
			plt.fill_between(x,p(x)+V,p(x)-V,color='m',alpha=0.2); 
		except:
			x = range(cuts[0],cuts[1]);
			z = np.polyfit(x,totalPer[cuts[0]:cuts[1]],1,cov=False);
			p = np.poly1d(z); 
			plt.plot(x,p(x),'m--');
	if(len(sumResponses['VI']) > cuts[1]+1):
		try:
			x = range(cuts[1],min(len(sumResponses['VI']),cuts[2]));
			z,V = np.polyfit(x,totalPer[cuts[1]:min(len(sumResponses['VI']),cuts[2])],1,cov=True);
			#V = 2*np.sqrt(V[1,1]); 
			V = sigma*np.std(totalPer[cuts[1]:min(len(sumResponses['VI']),cuts[2])])
			p = np.poly1d(z); 
			plt.plot(x,p(x),'m--');
			plt.fill_between(x,p(x)+V,p(x)-V,color='m',alpha=0.2); 
		except:
			x = range(cuts[1],min(len(sumResponses['VI']),cuts[2]));
			z = np.polyfit(x,totalPer[cuts[1]:min(len(sumResponses['VI']),cuts[2])],1,cov=False);
			p = np.poly1d(z); 
			plt.plot(x,p(x),'m--');


	plt.title("C-UAS {} Response Trends".format(semester))
	#plt.legend(legList);
	plt.xlabel("Project"); 
	plt.ylabel('# Responses')
	plt.axvline(8.5,c='k')
	plt.axvline(16.5,c='k')
	#plt.ylim([0,25]);
	if(save):
		#print("Saving")
		plt.savefig('{}SessionResponseTrends.png'.format(semester)); 
	else:
		plt.show(); 

	



if __name__ == '__main__':
	#getData(False); 
	fall2019GetData(True); 
	parseData(False); 
	sessionParse(False); 
	percentagePlots(False);
