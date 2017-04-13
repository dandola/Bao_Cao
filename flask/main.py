from flask import Flask, request
from object import *
import simpy
import random
from BroadcastPipe import *
from arrobject import *
app=Flask(__name__)
RANDOM_SEED=42
@app.route('/index',methods=['POST','GET'])
def index():
    if request.method=='POST':
        name1= (request.form['name1'])
        id1=int(request.form['id1'])
        name2=request.form['name2']
        id2=int(request.form['id2'])
        msg=request.form['msg']
        print("sender: %s      and      receiver: %s"%(name1,name2))
        random.seed(RANDOM_SEED)
        env=simpy.Environment()
        pipe=BroadcastPipe(env)
        dem=0
        # kiem tra nguoi gui co trong danh sach khong
        for x in arrobject:
            if x.name == name1 and x.id ==id1:
                print("%s has in list" %(name1))
                x.msg=msg
                source=x
                dem =1
                break
        # neu khong co thi tao moi
        if dem==0 :
            print("create a object: %s"% (name1))
            source= Computer(name1, id1)
            source.msg = msg
            arrobject.append(source)
        dem=0
        for x in arrobject:
            if x.name==name2 and x.id==id2:
                print("%s has in list" %(name2))
                des= x
                dem=1
                break
        if dem==0 :
            print("loi khong ton tai destination")
            return "error"
        env.process(source.send(des,env,pipe))
        env.process(des.receive(source,env,pipe.get_output_conn()))
        env.run()
        return "success"
if __name__=='__main__':
    app.run()
