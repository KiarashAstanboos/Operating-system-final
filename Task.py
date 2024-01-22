class task:

    def __init__(self,name,duration,arival,type):
        self.Name=name
        self.duration=duration
        self.arival=arival
        self.type=type # X Y Z
        self.state='ready' #ready/waiting/running
        self.doneTime=0
        self.waitedTime = 0
        if self.type=='X': self.priority=3
        elif self.type=='Y':self.priority=2
        elif self.type == 'Z':self.priority = 1
        else: raise Exception("invalid task type")

    def getRemainingTime(self):
        self.remainingTime=self.duration-self.doneTime
        return self.remainingTime


