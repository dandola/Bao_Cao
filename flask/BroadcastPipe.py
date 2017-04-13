import simpy
import random
class BroadcastPipe(object):
    def __init__(self,env,capacity=simpy.core.Infinity):
        self.env=env
        self.capacity=capacity
        self.pipes=[]   #pipes duoc coi nhu la mot bo nho dem trung gian giua recieve va send
    def put(self,value): #dung de broadcast 1 gia tri cho tat ca nguoi nhan
        if not self.pipes: #neu trong pipes khong co tin nhan -> thong bao loi.
            raise RuntimeError('there are no output pipes')
        events=[store.put(value) for store in self.pipes] #neu khong ta lay message co trong  pipes
        return self.env.all_of(events)
    def get_output_conn(self):  #dung de ket noi voi ben ngoai.
        pipe=simpy.Store(self.env,capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe
