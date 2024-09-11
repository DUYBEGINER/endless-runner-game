import Variables
import os

def update_score():
    if Variables.score > Variables.high_score:
        fo = open(os.path.join(Variables.current_dir, 'Main/High_Score'), 'w')
        fo.write(f'{Variables.score}')