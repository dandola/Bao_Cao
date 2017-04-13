import random
class Computer(object):
    a=10
    def __init__(self, name, id):
        self.name = name
        self.id=id

    def send(self,des,env,out_put):
        yield env.timeout(1)
        print("the computer has id = %d sent '%s' to the computer with id= %d at time %s"% (self.id,self.msg, des.id, str(env.now)))
        msg=(env.now, self.msg)
        out_put.put(msg)


    def receive(self,source,env,in_pipe):
        msg=yield in_pipe.get()
        yield env.timeout(10)
        print("the computer has id= %d received '%s' from computer with id=%d at time %d"% (self.id,msg[1],source.id,msg[0] + (env.now-msg[0])))
