class task:

    def __init__(self, name, duration, type):
        self.name = name
        self.burst = duration

        self.type = type  # X Y Z

        self.state = 'ready'  # ready/waiting/running
        self.doneTime = 0
        self.waitedTime = 0
        if self.type == 'X':
            self.priority = 3
        elif self.type == 'Y':
            self.priority = 2
        elif self.type == 'Z':
            self.priority = 1
        else:
            raise Exception("invalid task type")

        if self.type == 'X':
            self.need = [1,1,0]
        elif self.type == 'Y':
            self.need = [0,1,1]
        elif self.type == 'Z':
            self.need = [1,0,1]
        else:
            raise Exception("invalid task type")

    def getRemainingTime(self):
        self.remainingTime = self.burst - self.doneTime
        return self.remainingTime
