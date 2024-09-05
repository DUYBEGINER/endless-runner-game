import os

####### ĐỊNH NGHĨA CÁC BIẾN ########
# Thiết lập đường dẫn
current_dir_tmp = os.path.dirname(os.path.abspath(__file__)) #  Đường dẫn tới ../main
current_dir = os.path.dirname(current_dir_tmp) # Đường dẫn tới ../Game_project
# Kích thước cửa sổ game
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 500
# Kích thước các đối tượng trong game
GROUND_HEIGHT = 64      # Chiều dày mặt đất
BLOCK_SIZE = 32         # Kích thước khối block
# Trọng lực
GRAVITY = 0.25

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#........

#Các biến hành động nhân vật
moving_left = False
moving_right = False