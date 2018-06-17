'''
Program will run a basic monte carlo simulation on the group play matchups 
in group stage of world cup
'''


import random
from itertools import combinations 

# country objects will 
class Country():
	def __init__(self, n, wp):
		self.name = n
		self.winPercentage = wp
		self.points = 0
		self.advanced = 0
	def getCountry(self):
		return self.name
	def getStrengthRating(self):
		return self.winPercentage
	def getPoints(self):
		return self.points
	def resetPoints(self):
		self.points = 0
	def getAdvances(self):
		return self.advanced	
	def addPoints(self, p):
		self.points += p
	def addAdvances(self):
		self.advanced += 1
		

# number of group play simulations to run
simulation_iterations = 1000


# numbers associated with each country determine strength rating
# Note: values only matter relative to one another
countries = {'Russia': 4, 'Germany': 9.7, 'Brazil': 9.9, 
			'Portugal': 7.5, 'Argentina': 7.8, 'Belgium': 9.2, 
			'Poland': 5.5, 'France': 7.8, 'Spain': 9, 'Peru': 4, 
			'Switzerland': 6.4,  'England': 6.5,
			'Colombia': 5, 'Mexico': 5, 'Uruguay': 6, 
			'Croatia': 5.5, 'Denmark': 4.5, 'Iceland': 4, 
			'Costa Rica': 1, 'Sweden': 3, 'Tunisia': 2, 
			'Egypt': 2.4, 'Senegal': 2.4, 'Iran': 1.5, 'Serbia': 4,
			'Nigeria': 1.8, 'Australia': 2.6, 'Japan': 3, 
			'Morocco': 2, 'Panama': 1, 'South Korea': 2, 
			'Saudi Arabia': 1}
			
			
# arrays for each group 
groupATeams = ['Saudi Arabia', 'Russia', 'Egypt', 'Uruguay']
groupBTeams = ['Spain', 'Morocco', 'Iran', 'Portugal']
groupCTeams = ['France', 'Australia', 'Peru', 'Denmark']
groupDTeams = ['Argentina', 'Iceland', 'Croatia', 'Nigeria']
groupETeams = ['Brazil', 'Switzerland', 'Costa Rica', 'Serbia']
groupFTeams = ['Mexico', 'Sweden', 'South Korea', 'Germany']
groupGTeams = ['Belgium', 'Panama', 'Tunisia', 'England']
groupHTeams = ['Poland', 'Senegal', 'Colombia', 'Japan']


'''
function takes group array of strings and creates new 
array of country object for each country in group
'''
def createGroup(group, countries):
	new_group = []
	for team in group:
		# pass team name and strength rating to Country class
		new_group.append(Country(team, countries[team]))
	
	return new_group
	
# setup new arrays of country objects by group
groupA = createGroup(groupATeams, countries)
groupB = createGroup(groupBTeams, countries)
groupC = createGroup(groupCTeams, countries)
groupD = createGroup(groupDTeams, countries)
groupE = createGroup(groupETeams, countries)
groupF = createGroup(groupFTeams, countries)
groupG = createGroup(groupGTeams, countries)
groupH = createGroup(groupHTeams, countries)

groups =[ groupA, groupB, groupC, groupD,
		  groupE, groupF, groupG, groupH ]

# adds three points to country that wins in given matchup
def getWinner(country1, country2):
	sum_of_SRs = int((country1.getStrengthRating() + country2.getStrengthRating()))
	rand = random.randint(0, sum_of_SRs)

	if country1.getStrengthRating() > rand:
		country1.addPoints(1)
	else: country2.addPoints(1)


# when game is too close to determine random winner 
# is selected w/ randWinner()
def randWinner(team1, team2):
	r = random.randint(0,1)
	if r == 1: return team1
	else:      return team2


# find the winners of groups... most of code deals with situation when
# points are tied... note: simulation is simple and goals, ties, etc. 
# aren't tracked
def getGroupWinners(group):
	winner_index = 0
			
	for i in range(len(group)):
		if group[i].getPoints() >= group[winner_index].getPoints():
			if group[i].getPoints() == group[winner_index].getPoints():
				# if something is equal to the most then the higher ranking will be most
				# and the lower ranking must be moved down to next most
				if group[i].getStrengthRating() > group[winner_index].getStrengthRating():
					winner_index = i	
				elif group[i].getStrengthRating() == group[winner_index].getStrengthRating():
					if randWinner(group[i], group[winner_index]) == group[i]:
						winner_index = i	
			else:
				winner_index = i
					
	second_index = 0
	if winner_index == second_index: second_index = 1

	for i in range(len(group)):
		if i != winner_index:
			if group[i].getPoints() >= group[second_index].getPoints():
				if group[i].getPoints() == group[second_index].getPoints():
					if group[i].getStrengthRating() > group[second_index].getStrengthRating():
						second_index = i	
					elif group[i].getStrengthRating() == group[second_index].getStrengthRating():
						if randWinner(group[i], group[second_index]) == group[i]:
							second_index = i	
				else:
					second_index = i
	
	# record that which countries advanced to the next round in simulation
	# by storing in Country objects
	group[winner_index].addAdvances()
	group[second_index].addAdvances()
	

def groupPoints(group):	
	# comb is all the matches in the group play for a group
	comb = combinations(group, 2)
 
	# calculate the winner of each match in group and addign points
	for i in list(comb):
		getWinner(i[0], i[1])	


for i in range(simulation_iterations):		
	for group in groups:
		
		# calculate points for the group
		groupPoints(group)
		
		# find the winners in the group
		getGroupWinners(group)
		
		# reset points for teams in group
		for team in group:
			team.resetPoints()


# print results
for group in groups:
	for team in group:
		print(team.getCountry() + ": " + str(team.getAdvances()/10) + "%")
	print("")
	



			
