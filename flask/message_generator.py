# import random
# def message_generator(name,env,out_pipe,msg):
#         yield env.timeout(random.randint(6,10)) #tao ra 1 timeout
#         msg=(env.now,name + "say:"+ message +"at time"+ str(env.now))
#         out_pipe.put(msg)
#         message=message + msg[1]
