import math,random
def get_visible_thronglets(thronglet,others,range_=None):
    if range_ is None:
        range_=thronglet.detection_range+thronglet.traits.get('awareness',0)//2
    return[t for t in others if t.alive and t!=thronglet and math.hypot(t.x-thronglet.x,t.y-thronglet.y)<=range_]

def select_social_target(thronglet,visible):
    if not visible:return None
    if thronglet.personality=='aggressive':
        return max(visible,key=lambda t:t.traits['strength'])
    elif thronglet.personality=='timid':
        return min(visible,key=lambda t:math.hypot(t.x-thronglet.x,t.y-thronglet.y))
    elif thronglet.personality=='curious':
        return random.choice(visible)
    elif thronglet.personality=='protective':
        return min(visible,key=lambda t:t.hp)
    elif thronglet.personality=='selfish':
        return max(visible,key=lambda t:t.food+t.water)
    return random.choice(visible)

def init_social(thronglet):
    thronglet.relationships={}
    thronglet.group_id=None

def update_relationships(thronglet,visible):
    for other in visible:
        key=f'{other.x}_{other.y}'
        if key not in thronglet.relationships:
            thronglet.relationships[key]=random.randint(1,5)
        else:
            delta=random.choice([-1,0,1])
            thronglet.relationships[key]=max(0,min(10,thronglet.relationships[key]+delta))

def get_close_allies(thronglet,threshold=7):
    return[key for key,value in thronglet.relationships.items()if value>=threshold]

def assign_group(thronglet,group_id):
    thronglet.group_id=group_id