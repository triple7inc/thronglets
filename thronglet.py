from traits import generate_traits,assign_personality,apply_personality_traits
from behavior import decide_movement
from behavior import decide_reaction
from social import init_social
import random,math,json,os
class Thronglet:
    def __init__(self,x,y,hp=100,speed=1,detection_range=None,avoidance_speed=None,relationships=None):
        self.x=x
        self.y=y
        self.hp=hp
        self.age=0
        self.food=50
        self.water=50
        self.bump_xp=0
        self.alive=True
        self.speed=speed
        self.group_id=None
        self.genetic_code=''
        self._all_thronglets=[]
        self.traits=generate_traits()
        self.personality=assign_personality()
        self.traits=apply_personality_traits(self.traits,self.personality)
        self.relationships=relationships if relationships is not None else {}
        self.avoidance_speed=avoidance_speed if not avoidance_speed is None else random.randint(2,4)+self.traits.get('agility',0)//3
        self.detection_range=detection_range if not detection_range is None else random.randint(3,6)+self.traits.get('awareness',0)//2
        init_social(self)

    def to_dict(self):
        return{
            'x':self.x,
            'y':self.y,
            'hp':self.hp,
            'speed':self.speed,
            'detection_range':self.detection_range,
            'avoidance_speed':self.avoidance_speed,
            'food':self.food,
            'water':self.water,
            'alive':self.alive,
            'traits':self.traits,
            'personality':self.personality,
            'genetic_code':self.genetic_code,
            'relationships':self.relationships,
            'age':self.age if hasattr(self,'age') else 0,
            'group_id':(self.group_id if not self.group_id is None else -1) if hasattr(self,'group_id') else -1
        }

    def move(self,grid_w,grid_h,danger_x=None,danger_y=None):
        if not self.alive:return
        decide_movement(self,grid_w,grid_h,danger_x,danger_y)

    def in_range(self,d_x,d_y):
        return math.hypot(self.x-d_x,self.y-d_y)<=self.detection_range

    def react_event(self,event):
        decide_reaction(self,event)

    def bump(self,other):
        if abs(self.x-other.x)<=1 and abs(self.y-other.y)<=1:
            self.hp-=5
            other.hp-=5
            self.bump_xp+=1
            other.bump_xp+=1
            if self.hp<=0:self.alive=False
            if other.hp<=0:other.alive=False

    def evolve(self,parent=None):
        if parent:
            self.speed=parent.speed if random.random()>0.5 else random.randint(1,3)
            self.hp=parent.hp if random.random()>0.5 else random.randint(80,100)
            self.detection_range=parent.detection_range if random.random()>0.5 else random.randint(2,6)
            self.avoidance_speed=parent.avoidance_speed if random.random()>0.5 else random.uniform(1,2)
            self.traits=generate_traits(parent.traits)
            self.personality=parent.personality
            self.traits=apply_personality_traits(self.traits,self.personality)
            if hasattr(parent,'bump_xp')and parent.bump_xp>0:
                self.hp+=min(parent.bump_xp*2,20)
                if parent.bump_xp>=3:self.detection_range+=1
            self.bump_xp=0
        self.genetic_code=f'speed:{self.speed},detection:{self.detection_range},avoidance:{self.avoidance_speed}'

    def fitness(self):
        return (self.hp/100)+(1 if self.hp>0 else 0)

    def save_data(self,filename):
        data={'x':self.x,'y':self.y,'hp':self.hp,'speed':self.speed,'alive':self.alive,
              'food':self.food,'water':self.water,'detection_range':self.detection_range,
              'avoidance_speed':self.avoidance_speed,'genetic_code':self.genetic_code}
        with open(filename,'w')as f:json.dump(data,f)

    def load_data(self,filename):
        if not os.path.exists(filename):return
        with open(filename,'r')as f:data=json.load(f)
        self.__dict__.update(data)

    def save_genetic_code(self,directory='logs'):
        if not os.path.exists(directory):os.makedirs(directory)
        filename=f'{directory}/thronglet_code_{self.x}_{self.y}.txt'
        with open(filename,'w')as f:f.write(self.genetic_code)

def gen_population(size,grid_w,grid_h):
    return[Thronglet(random.randint(0,grid_w-1),random.randint(0,grid_h-1))for _ in range(size)]

def evolve_population(pop,grid_w,grid_h,mutation_chance=0.1):
    if not pop:return[]
    survivors=[t for t in pop if t.alive]
    if not survivors:return[]
    sorted_pop=sorted(survivors,key=lambda t:t.fitness(),reverse=True)
    new_gen=[]
    count=max(1,len(sorted_pop)//2)
    for i in range(count):
        if i>=len(sorted_pop):break
        parent=sorted_pop[i]
        fitness=parent.fitness()
        fertility=max(1,parent.traits.get('fertility',3))
        base_offspring=1 if fitness<1 else 2 if fitness<1.5 else 3
        bonus=random.randint(0,fertility//2)
        n=base_offspring+bonus
        for _ in range(n):
            if random.random()<0.05:continue
            dx=random.choice([-1,0,1])
            dy=random.choice([-1,0,1])
            child=Thronglet((parent.x+dx)%grid_w,(parent.y+dy)%grid_h)
            child.traits=generate_traits(parent.traits,mutation_chance)
            child.personality=parent.personality
            child.traits=apply_personality_traits(child.traits,child.personality)
            child.avoidance_speed=max(0.5,child.avoidance_speed)
            child.evolve(parent)
            new_gen.append(child)
    if len(new_gen)==0 and survivors:
        dx=random.choice([-1,0,1])
        dy=random.choice([-1,0,1])
        parent=random.choice(survivors)
        child=Thronglet((parent.x+dx)%grid_w,(parent.y+dy)%grid_h)
        child.traits=generate_traits(parent.traits,0.2)
        child.personality=parent.personality
        child.traits=apply_personality_traits(child.traits,child.personality)
        child.avoidance_speed=max(0.5,child.avoidance_speed)
        child.evolve(parent)
        new_gen.append(child)
    return new_gen

def fire_event(pop,x,y,radius=3,max_dmg=20):
    for t in pop:
        dist=math.hypot(t.x-x,t.y-y)
        if dist<=radius:
            dmg=max_dmg-(dist*(max_dmg/radius))
            t.hp-=dmg
            if t.hp<=0:t.alive=False

def rock_event(pop,x,y,radius=3):
    for t in pop:
        if math.hypot(t.x-x,t.y-y)<=radius:
            t.hp=0
            t.alive=False

def save_generation(pop,gen_num,directory='logs'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    data=[]
    for t in pop:
        if not t.alive:
            continue
        data.append(t.to_dict())

    with open(f'{directory}/generation_{gen_num}.json', 'w') as f:
        json.dump(data, f)

def load_generation(gen_num, directory='logs'):
    filename=f'{directory}/generation_{gen_num}.json'
    if not os.path.exists(filename):
        return []

    with open(filename, 'r') as f:
        data=json.load(f)

    pop=[]
    for d in data:
        t=Thronglet(
            x=d['x'],
            y=d['y'],
            hp=d['hp'],
            speed=d['speed'],
            detection_range=d['detection_range'],
            avoidance_speed=d['avoidance_speed']
        )
        t.food=d['food']
        t.water=d['water']
        t.alive=d['alive']
        t.genetic_code=d['genetic_code']
        t.traits=d['traits']
        t.personality=d['personality']
        t.relationships=d.get('relationships',{})

        pop.append(t)
    return pop

def save_genetic_codes(pop,log_dir='logs'):
    if not os.path.exists(log_dir):os.makedirs(log_dir)
    for t in pop:
        if t.alive:
            filename=f'{log_dir}/thronglet_code_{t.x}_{t.y}.txt'
            with open(filename,'w')as f:
                f.write(t.genetic_code)