# ESP32 MicroPython - OpenBot Parser (Arduino Style)
import sys
import time

print("ESP32 OpenBot Parser - Arduino Style")
print("Sẵn sàng nhận lệnh từ điện thoại...")
print("-" * 60)

# State machine constants
HEADER = 0
BODY   = 1

class OpenBotParser:
    def __init__(self):
        self.msg_part = HEADER    # HEADER hoặc BODY
        self.header   = ''        # Ký tự header ('c','i','l',...)
        self.msg_buf  = ''        # Phần body thu được
        
        # Lưu trữ dữ liệu target
        self.target_x = 0
        self.target_y = 0
        self.target_w = 0
        self.target_h = 0
        self.img_width = 0
        self.img_height = 0
        self.has_target = False   # Flag để biết có target data không

    def parse_msg(self):
        """Xử lý message khi đã đầy đủ header + body"""
        h   = self.header
        buf = self.msg_buf

        # bounding box:
        if h == 't':  # Target / bounding box: t<x>,<y>,<w>,<h>,<imgW>,<imgH>
            try:
                parts = buf.split(',')
                if len(parts) == 6:
                    self.target_x, self.target_y, self.target_w, self.target_h, self.img_width, self.img_height = map(int, parts)
                    self.has_target = True
                    print(f"Target: x={self.target_x}, y={self.target_y}, w={self.target_w}, h={self.target_h}, imgW={self.img_width}, imgH={self.img_height}")
                else:
                    print("[ERROR] Invalid target format:", buf)
                    self.has_target = False
            except:
                print("[ERROR] Exception parsing target:", buf)
                self.has_target = False

        self.msg_part = HEADER
        self.header   = ''
        self.msg_buf  = ''

    def process_char(self, char):
        """Xử lý từng ký tự vào state machine"""
        if char in ('\n', '\r'):
            # Kết thúc message -> parse
            if self.header:
                self.parse_msg()
            return

        if self.msg_part == HEADER:
            # header mới
            self.header   = char
            self.msg_part = BODY
            self.msg_buf  = ''
        else:
            # Đang thu body
            self.msg_buf += char

    def get_target_x(self):
        """Lấy tọa độ x của target"""
        print("Lấy tọa độ x của target:", self.target_x)
        return self.target_x if self.has_target else None
    
    def get_target_y(self):
        """Lấy tọa độ y của target"""
        print("Lấy tọa độ y của target:", self.target_y)
        return self.target_y if self.has_target else None
    
    def get_target_w(self):
        """Lấy chiều rộng của target"""
        print("Lấy chiều rộng của target:", self.target_w)
        return self.target_w if self.has_target else None
    
    def get_target_h(self):
        """Lấy chiều cao của target"""
        print("Lấy chiều cao của target:", self.target_h)
        return self.target_h if self.has_target else None
    
    def get_target_box(self):
        """Lấy toàn bộ bounding box (x, y, w, h)"""
        print("Lấy bounding box của target:", (self.target_x, self.target_y, self.target_w, self.target_h))
        if self.has_target:
            return (self.target_x, self.target_y, self.target_w, self.target_h)
        return None
    
    def get_image_size(self):
        """Lấy kích thước ảnh (width, height)"""
        print("Lấy kích thước ảnh:", (self.img_width, self.img_height))
        if self.has_target:
            return (self.img_width, self.img_height)
        return None
    
    def is_target_available(self):
        """Kiểm tra có target data không"""
        print("Kiểm tra có target data:", self.has_target)
        return self.has_target

# # --- Main Loop ---
# parser = OpenBotParser()

# # Example usage trong main loop
# def check_target_data():
#     """Ví dụ sử dụng các getter functions"""
#     if parser.is_target_available():
#         x = parser.get_target_x()
#         y = parser.get_target_y() 
#         w = parser.get_target_w()
#         h = parser.get_target_h()
        
#         box = parser.get_target_box()
#         img_size = parser.get_image_size()
        
#         print(f"Individual: x={x}, y={y}, w={w}, h={h}")
#         print(f"Box: {box}")
#         print(f"Image size: {img_size}")

# while True:
#     try:
#         data = sys.stdin.read(1) if hasattr(sys.stdin, 'read') else input()
        
#         for ch in data:
#             parser.process_char(ch)
            
#     except KeyboardInterrupt:
#         print("\nDừng chương trình...")
#         break
#     except Exception as e:
#         time.sleep(0.01)