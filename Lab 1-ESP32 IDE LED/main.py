from machine import Pin  # Thêm thư viện các chân kết nối đã định nghĩa
from time import sleep_ms  # Thêm thư viện tạo độ trễ theo mili giây

led = Pin(2, Pin.OUT)  # Gán chân 2 là ngõ ra Led
sw = Pin(19, Pin.IN)  # Gán chân 19 là tín hiệu ngõ vào, với chế độ kéo lên nội

# Đặt mặc định ban đầu tắt LED
led.value(0)

# Trạng thái hiện tại của nút nhấn
previous_sw_status = sw.value()

while True:  # Tạo vòng lặp vô hạn
    sw_status = sw.value()  # Lưu tín hiệu ngõ vào vào một biến

    if sw_status != previous_sw_status:  # Chỉ khi trạng thái thay đổi mới thực hiện in ra console
        previous_sw_status = sw_status
        print('Trạng thái nút nhấn:', sw_status)

    if sw_status == 0:  # Nếu trạng thái nút nhấn bằng 0 thì chuyển chế độ chớp tắt Led
        led.value(1)
        sleep_ms(500)  # Dùng sleep_ms để giảm thời gian xử lý
        led.value(0)
        sleep_ms(500)
    else:  # Nếu trạng thái nút nhấn khác 0 thì chuyển chế độ tắt Led
        led.value(0)
        sleep_ms(10)  # Giảm thời gian ngủ để tăng độ nhạy cho việc phát hiện nhấn nút
        # Đợi cho đến khi nút được nhấn
        while sw.value() == 1:
            pass
