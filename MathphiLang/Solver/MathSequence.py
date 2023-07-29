

class MathSequence(object):

    def __init__(self)->None:
        self._steps = []
        self._descriptions = []
        self._header = ''
        self._sequence = list(tuple())
    @property
    def sequence(self):
        return self._sequence
    
    @sequence.setter
    def sequence(self, s):
        raise Exception('sequence is a read-only property')
    
    @property
    def header(self):
        return self._header
    
    @header.setter
    def header(self, h):
        self._header = h
    @property
    def steps(self):
        return self._steps
    
    @steps.setter
    def steps(self, s):
        self._steps = s
    
    @property
    def descriptions(self):
        return self._descriptions
    
    @descriptions.setter
    def descriptions(self, d):
        self._descriptions = d
    
    def push_step(self,step):
        self._steps.append(step)

    def push_description(self,des):
        self._descriptions.append(des)

    def push(self,s,d):
        self.push_step(s)
        self.push_description(d)

    def construct_sequence(self):
        if len(self._steps)- len(self._descriptions) == 1:
            sequence = list(tuple())
            pre_step = self._steps[0]
            last_step = self._steps[len(self._steps)-1]
            pre_des = self._descriptions[0]
            for s,d in zip(self._steps,self._descriptions):
                if s == self._steps[0] and d == self._descriptions[0]:
                    continue
                sequence.append((pre_step,pre_des,s))
                pre_des = d
                pre_step = s
            sequence.append((pre_step,pre_des,last_step))
            self._sequence = sequence
        else:
            raise Exception('steps should be compatible with descriptions')
    


