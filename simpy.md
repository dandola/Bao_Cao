# kiến thức cơ bản về Simpy
## 1. kiến thức cơ bản
### a. các khái niệm cơ bản
 - simpy là một thư viện mô phỏng các sự kiện rời rạc. hành vi của các thành phần hoạt đọng được mô hình bằng các tiến trình. tất cả các tiến trình nằm trong cùng một môi trường (env). chúng tương tác với môi trường và với nhau qua các sự kiện.
 - khi tạo ra một tiến trình, tiến trình sẽ bị tạm dừng. Simpy tiếp tục xử lý, khi sự kiện xảy ra (sự kiện được kích hoạt).Nhiều tiến trình có thể chờ đợi cùng một sự kiện. Simpy tiếp tục chúng theo thứ tự mà chúng đã tạo ra sự kiện đó.
- có một loại sự kiện quan trọng là `Timeout`. sự kiện này cho phép một tiến trình tạm ngưng trong một khoảng thời gian cho phép và được gọi bằng cú pháp  `env.timeout(time)` trong đó `env` là biến được khởi tạo bởi môi trường (`Environment`), `time` là thời gian mà tạm ngưng của một trạng thái nào đó.
```sh 
vd: 
>>> import simpy
>>> def car(env):
            while True:
                print("Start parking at %d "% env.now)
                parking_duration=5
                yield env.timeout(parking_duration)
                print("Start driving at %d"% env.now)
                trip_duration=2
                yield env.timeout(trip_duration)
>>> env=simpy.Environment()
>>> env.process(car(env))
>>> env.run(until=15)
```
ví dụ trên là mô phỏng quá trình hoạt động của car, trong đó car có 2 hoạt động chính là parking và driving, với mỗi hoạt động parking( or driving), nó sẽ sinh ra một `timeout` cho từng hoạt động đó, sau khoảng thời gian `timeout`, nó đưa ra một tin nhắn và thời gian mô phỏng hiện tại thông qua `env.now()`.
    
  Như vậy để bắt đầu thực hiện, đầu tiên cần phải tạo ra một môi trường (`env=simpy.Environment()`). sau khi tạo ra mội môi trường, để có thể bắt đầu thực hiện mô phỏng trong môi trường đó,cần phải được thêm vào trong môi trường thông qua `Environment.process()`

  và cuối cùng quá trình mô phỏng được bắt đầu với câu lệnh `env.run(until=15)` với  `until=15` là khoảng thời gian mô phỏng.
# b. tiến trình tương tác
giữa hai tiến trình có thể có sự tương tác với nhau
có hai cách biểu diễn sự tương tác giữa các tiến trình:

        + tiến trình  này chờ đợi một tiến trình khác kết thúc
        + tiến trình này có thể làm gián đoạn tiến trình khác.
## **chờ đợi một tiến trình** 
sự tương tác này đơn giản chỉ là một tiến trình được bắt đầu sau khi một tiến trình khác trước nó kết thúc. hãy tưởng tượng mô phỏng việc xe ô tô phải sạc pin, khi hết chỗ sạc, thì nó phải đợi một chiếc xe khác hoàn thành xong việc sạc pin, rồi mới đến lượt nó.
## **làm gián đoạn tiến trình khác**
```c
>>> import simpy
>>> class Car(object):
        def __init__(self, env):
                self.env = env
                self.action = env.process(self.run())
        def run(self):
                while True:
                   print("Start parking and charging at %d"% self.env.now)
                   charge_duration=5
                   try:
                   yield self.env.process(self.charge(charge_duration))
                   except simpy.Interrupt:
                   print('Was interrupted. Hope, the battery is full enough ...')
                   print('Start driving at %d' % self.env.now)
                   trip_duration=2
                   yield self.env.timeout(trip_duration)
        def charge(self,duration):
                yield self.env.timeout(duration)
>>> def driver(env,car):
        yield rnv.timeout(3)
        car.action.interrup()
>>> env=simpy.Environment()
>>> car=Car(env)
env.process(driver(env,car))
>>> env.run(until=15)
```

ví dụ trên mô phỏng việc một đối tượng car có thể thực hiện các thao tác là `driving` hoắc `charging`.   
giả sử rằng khi chương trình chạy thì đối tượng car sẽ thực hiện thao tác `charge()` đầu tiên, thông thường car sẽ được nạp pin đầy thì hoạt động `driving` mới được thực hiện.   
simpy cho phép bạn có thể làm gián đoạn(interrup) 1 tiến trình khi nó đang chạy bằng câu lệnh `interrupt()`.   
như vậy giả sử rằng khi car đang thực hiện `charging` với thời gian là 5p mới có thể đầy pin, nếu bạn muốn thực hiện `driving` khi mà công việc `charging`(sạc điện) chưa hoàn thành, bạn có thể sử dụng `interrupt` để có thể ngắt nó.   
Kết quả là trước đây bạn phải mất  thời gian là 5p để `charging` mới có thể thực hiện `driving` thì bây giờ bạn có thể bắt đầu `driving` khi mà `charging` vẫn chưa hoàn thành.
### c. chia sẻ tài nguyên
```sh
>>> import simpy
>>> def car(env,name,bcs,driving_time,charge_duration):
        yield env.timeout(driving_time)
        print("%s arriving at %d"% (name,env.now))
        with bcs.request() as req:
            yield req
            print('%s starting to charge at %s' % (name, env.now))
            yield env.timeout(charge_duration)
            print('%s leaving the bcs at %s' % (name, env.now))
>>> env=simpy.Environment()
>>> bcs=simpy.Resource(env,capacity=2)
>>> for i in range(4):
        env.process(car(env, 'Car %d' % i, bcs, i*2, 5))
>>> env.run()
```
- Ví dụ trên mô phỏng quá trình chiếc xe tới một trạm sạc pin (bcs) và yêu cầu một trong hai điểm nạp. nếu cả hai được sử dụng thì nó sẽ đợi cho đến khi 1 trong 2 trở nên khả dụng.
- Ở ví dụ trên chúng ta sử dụng class `Resource` của simpy. phương thức `request()` của Resource cho phép nó chờ đợi cho đến khi tài nguyên khả dụng. với câu lệnh `with` phía trên thì sau khi hoàn thành vông việc, tài nguyên sẽ tự động giả phóng. Nếu không sử dụng `with` thì sau khi sử dụng tài nguyên xong, phải sử dụng lệnh `release()` để giải phóng tài nguyên.





