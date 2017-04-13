# import random
# def message_consumer(name,env,in_pipe,message):
#         msg=yield in_pipe.get()
#         string="hello world"
#         if msg[0]<env.now:
#              message+="Later getting message: at time" + str(env.now) + ":"+ name+ "recieved message:"+ msg[1]
#             #  print(message)
#         else:
#              message+="at time"+ str(env.now) + ":"+ name+" recieved message:"+ msg[1]
#         # yield env.timeout(random.randint(4,8))
