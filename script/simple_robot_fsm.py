################################################################
# Include Module
################################################################
from random import randint
import time

################################################################
# Transition
################################################################
class Transition(object):
	def __init__(self,toState):
		self.toState = toState
	def Execute(self):
		print("Transition ...")
################################################################

################################################################
# State
################################################################
class State(object):
	def __init__(self,FSM):
		self.FSM = FSM
		self.timer = 0
		self.startTime = 0
	def Enter(self):
		self.timer = randint(0,5)
		self.startTime = int(time.time())
	def Execute(self):
		pass
	def Exit(self):
		pass
################################################################

################################################################
# CleanDishes
################################################################
class CleanDishes(State):
	def __init__(self,FSM):
		super(CleanDishes,self).__init__(FSM)
	def Enter(self):
		print("Preparing to clean dishes")
		super(CleanDishes,self).Enter()
	def Execute(self):
		print("Cleaning dishes")
		if(self.startTime + self.timer <= time.time()):
			if not(randint(1,3)%2):
				self.FSM.Transition("toVacum")
			else:
				self.FSM.Transition("toSleep")
	def Exit(self):
		print("Finished cleaning dishes ...")
################################################################

################################################################
# Vacuum
################################################################
class Vacuum(State):
	def __init__(self,FSM):
		super(Vacuum,self).__init__(FSM)
	def Enter(self):
		print("Starting to Vacuum")
		super(Vacuum,self).Enter()
	def Execute(self):
		print("Vacuuming")
		if(self.startTime + self.timer <= time.time()):
			if not (randint(1,3)%2):
				self.FSM.Transition("toSleep")
			else:
				self.FSM.Transition("toCleanDishes")
	def Exit(self):
		print("Finished Vacuuming")
################################################################

################################################################
# Sleep
################################################################
class Sleep(State):
	def __init__(self,FSM):
		super(Sleep,self).__init__(FSM)
		self.sleepAmount = 0
		self.startTime = 0
	def Enter(self):
		print("Starting to Sleep")
		super(Sleep,self).Enter()
	def Execute(self):
		print("Sleeping")
		if(self.startTime + self.timer <= time.time()):
			if not (randint(1,3)%2):
				self.FSM.Transition("toVacuum")
			else:
				self.FSM.Transition("toCleanDishes")
	def Exit(self):
		print("Waking up from Sleep")
################################################################

################################################################
# Finite State Machines
################################################################
class FSM(object):
	def __init__(self,character):
		self.char = character
		self.states = {}
		self.transitions = {}
		self.curState = None
		self.prevState = None #use to prevent looping 2 state
		self.trans = None
	def AddTransition(self,transName,transition):
		self.transitions[transName] = transition
	def AddState(self,stateName,state):
		self.states[stateName] = state
	def SetState(self,stateName):
		self.prevState = self.curState
		self.curState = self.states[stateName]
	def Transition(self,toTrans):
		self.trans = self.transitions[toTrans]
	def Execute(self):
		if(self.trans):
			self.curState.Exit()
			self.trans.Execute()
			self.SetState(self.trans.toState)
			self.curState.Enter()
			self.trans = None
		self.curState.Execute()
################################################################

################################################################
# Implementation
################################################################
Char = type("Char",(object,),{})

class RobotMaid(Char):
	def __init__(self):
		self.FSM = FSM(self)
		# states
		self.FSM.AddState("Sleep",Sleep(self.FSM))
		self.FSM.AddState("CleanDishes",CleanDishes(self.FSM))
		self.FSM.AddState("Vacuum",Vacuum(self.FSM))
		# transitions
		self.FSM.AddTransition("toSleep",Transition("Sleep"))
		self.FSM.AddTransition("toVacuum",Transition("Vacuum"))
		self.FSM.AddTransition("toCleanDishes",Transition("CleanDishes"))

		self.FSM.SetState("Sleep")
	def Execute(self):
		self.FSM.Execute()
################################################################

# class Test():
# 	def __init__(self) -> None:
# 		self.Name = {}
# 	def AddName(self,NameKey,NameValue):
# 		self.Name[NameKey] = NameValue

# t = Test()
# t.AddName("Nontanan","Sommat")
# t.AddName("Sudarat","Rodsee")
# print(t.Name)
		
################################################################
# Main Code
################################################################
if __name__ == "__main__":
	robot = RobotMaid()
	for i in range(20):
		startTime = time.time()
		timeInterval = 1
		print(robot.FSM.transitions)
		print("################################################################")
		while(startTime + timeInterval > time.time()):
			pass
		robot.Execute()
################################################################