import pygame, random, os, json
from pygame.sprite import Sprite
from pygame.sprite import Group
import Variables


# Định nghĩa một số biêns liên quan
GRAVITY_STONE = 0.025
MAX_HIGH = 4  # Định nghĩa độ cao cột đá có thể có
SETTINGS_FILE = 'settings.json'  # Tên tệp lưu trữ cài đặt
global difficulty

with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            difficulty = settings.get('difficulty')
# Định nghĩa nhóm các viên đá
stones = Group()
# Define Class Stone_fall
class Stone(Sprite):
    def __init__(self, scale, stone_type):
        Sprite.__init__(self)
        self.type = stone_type
        # Load image stone
        img_stone_fall = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Map/{stone_type}.png'))
        # Create Rect of stone_fall
        self.scale = scale
        self.image = pygame.transform.scale(img_stone_fall,(img_stone_fall.get_width() * scale, img_stone_fall.get_height() * scale))
        self.rect = self.image.get_rect()
        if difficulty == 'Easy':
            self.dfc = 1.0
        elif difficulty == 'Normal':
            self.dfc = 1.25
        elif difficulty == 'Hard':
            self.dfc = 1.5
        elif difficulty == 'Hardest':
            self.dfc = 2
        
        tmp = random.randint(1, 8)  # Lấy một số ngẫu nhiên từ 1 đến 8 để làm giá trị x ban đầu cho stone
        # Kiểm tra để lấy vị trí spawn để không gây trường hợp xấu
        while (not self.check_high(tmp)):
            tmp = self.check_min_high()
        self.rect.center = (tmp * self.image.get_width() + self.image.get_width() / 2, -10)
        # Định nghĩa các biến liên quan đến rơi
        self.in_air = True
        self.vel_y = 0
        self.MAX_VEL = 4
        # Định nghĩa các biến liên quan đến xóa các đối tượng
        self.list_to_delete = []
        self.list_to_check_high = []

    # Định nghĩa các phương thức của class
    def update(self):
        dy = 0
        # Kiểm tra đá có chạm mặt đất hay chưa
        if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
            self.in_air = False
            self.vel_y = 0
            self.rect.bottom = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT + 1
        else:
            self.in_air = True
        # Tính toán tốc độ rơi của đá
        self.check_collision_otherStone()
        # Áp dụng 
        if (self.in_air):
            self.vel_y += GRAVITY_STONE * self.dfc
            if self.vel_y > self.MAX_VEL * self.dfc:
                self.vel_y = self.MAX_VEL * self.dfc
        dy = self.vel_y
        self.rect.centery += dy
        # Kiểm tra và xóa các đối tượng chạm mặt đâts nếu đủ điều kiện
        self.check_to_delete_fall2()
        self.check_to_delete()

    def check_collision_otherStone(self):
        for i in stones:
            if self != i:
                if (self.rect.centerx < i.rect.right and
                        self.rect.centerx > i.rect.left and
                        self.rect.bottom <= i.rect.top + 5 and
                        self.rect.bottom >= i.rect.top):
                    self.in_air = False
                    self.vel_y = 0
                    self.rect.bottom = i.rect.top + 1
                    break
                else:
                    self.in_air = True

    def check_to_delete(self):
        # reset list_to_delete
        self.list_to_delete = []
        for i in stones:
            if (i.rect.bottom >= Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT - 2):
                self.list_to_delete.append(i)
        if len(self.list_to_delete) == 8:
            for i in self.list_to_delete:
                i.kill()

    def check_to_delete_fall2(self):
        # Kiểm tra đối tượng là đá rơi dạng 2 và in_air là False
        if self.type == 'stone_fall2':
            for i in stones:
                if self != i:  # Đảm bảo không so sánh với chính nó
                    # Kiểm tra va chạm giữa self và i
                    # if self.rect.colliderect(i.rect):
                    # Kiểm tra nếu i (đối tượng khác) đang rơi vào self
                    if (self.rect.centerx < i.rect.right and
                            self.rect.centerx > i.rect.left and
                            self.rect.top < i.rect.bottom + 1):
                        self.kill()
                        break
    def check_high(self, x):
        # reset list_to_check_high
        self.list_to_check_high = []
        pos_x = x * self.rect.width + self.rect.width / 2
        for i in stones:
            if abs(i.rect.centerx - pos_x) < self.rect.width:
                self.list_to_check_high.append(i)
        return (len(self.list_to_check_high) < MAX_HIGH)

    def check_min_high(self):
        # Khởi tạo các biến liên quan
        min_col = -1
        tmp_min = float('inf')  # Sử dụng giá trị vô cực để bắt đầu tìm số lượng đá ít nhất
        # reset list_to_check_high
        self.list_to_check_high = []
        # Kiểm tra từng cột từ 1 đến 8
        for col in range(1, 9):
            pos_x = col * self.rect.width + self.rect.width / 2
            self.list_to_check_high = []

            # Kiểm tra từng viên đá trong danh sách `stones`
            for stone in stones:
                # Kiểm tra xem viên đá có nằm trong cột hiện tại không
                if abs(stone.rect.centerx - pos_x) < self.rect.width:
                    self.list_to_check_high.append(stone)

            # Cập nhật cột có số lượng đá ít nhất
            if len(self.list_to_check_high) < tmp_min:
                tmp_min = len(self.list_to_check_high)
                min_col = col
        return min_col