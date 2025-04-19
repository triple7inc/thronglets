import random,math
from social import get_visible_thronglets,select_social_target
def decide_movement(thronglet,grid_w,grid_h,danger_x=None,danger_y=None):
    if not thronglet.alive:return

    px,py=thronglet.x,thronglet.y
    speed=thronglet.speed+thronglet.traits['agility']//4
    avoid=thronglet.avoidance_speed+thronglet.traits['agility']//3
    detection=thronglet.detection_range+thronglet.traits['awareness']//3
    ax=ay=0

    if danger_x!=None and danger_y!=None:
        dist=math.hypot(px-danger_x,py-danger_y)
        if dist<=detection:
            if thronglet.personality=='timid' or dist<thronglet.traits['resilience']+2:
                ax=-1 if px<danger_x else 1
                ay=-1 if py<danger_y else 1
                thronglet.x=(px+ax*avoid)%grid_w
                thronglet.y=(py+ay*avoid)%grid_h
                return

    visible=get_visible_thronglets(thronglet,thronglet._all_thronglets,detection)
    target=select_social_target(thronglet,visible)if visible else None

    if target:
        dx=1 if target.x>px else -1 if target.x<px else 0
        dy=1 if target.y>py else -1 if target.y<py else 0
        ax,ay=dx,dy
    elif thronglet.personality=='curious' and random.random()<0.5:
        ax,ay=random.choice([-1,1]),random.choice([-1,1])
    elif thronglet.personality=='aggressive':
        ax=1 if random.random()<0.7 else -1
        ay=1 if random.random()<0.7 else -1
    else:
        ax=random.choice([-1,1])
        ay=random.choice([-1,1])

    thronglet.x=(px+ax*speed)%grid_w
    thronglet.y=(py+ay*speed)%grid_h

def decide_reaction(thronglet,event):
    if not thronglet.alive:return
    dmg=0

    if event=='fire':
        base=20
        resist=thronglet.traits['resilience']
        if thronglet.personality=='timid':resist+=1
        dmg=max(0,base-resist*2)
        thronglet.hp-=dmg

    elif event=='rock':
        luck=thronglet.traits['agility']+thronglet.traits['awareness']
        if thronglet.personality=='curious':luck-=1
        survive_chance=luck/20
        if random.random()>survive_chance:
            thronglet.hp=0
        else:
            thronglet.hp-=20-thronglet.traits['resilience']

    if thronglet.hp<=0:thronglet.alive=False
