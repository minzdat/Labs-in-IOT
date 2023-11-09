from machine import Pin #Thêm thư viện các chân kết nối đã định nghĩa
from time import sleep #Thêm thư viện tạo độ trễ
led = Pin(12, Pin.OUT) #Gán chân 12 là ngõ ra Led
sw=Pin(19,Pin.IN) #Gán chân 19 là tín hiệu ngõ vào 
while True: #Tạo vòng lặp vô hạn 
  sw_status=sw.value() #Lưu tín hiệu ngõ vào là vào một biến
  if sw_status > 0: #Nếu trạng thái nút nhấn khác 0 thì chuyển chế độ chớp tắt Led
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
    print('Chế độ 1:', sw_status)
    print('Chế độ 2:', sw.value())
  elif sw_status == 0: #Nếu trạng thái nút nhấn bằng 0 thì chuyển chế độ tắt Led
    led.value(0)
    sleep(0.5)
    while sw.value() == 0:
        print('Chế độ 1:', sw_status)
        print('Chế độ 2:', sw.value())
        pass  # Đợi cho đến khi nút được nhấn