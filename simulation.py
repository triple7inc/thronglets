from thronglet import Thronglet,gen_population,evolve_population,fire_event,rock_event,save_generation,load_generation,save_genetic_codes
from traits import generate_traits,assign_personality,apply_personality_traits
from social import get_visible_thronglets
import json,os,random,math,shutil,zipfile
from groups import form_groups
import gc

with open('config.json','r')as f:cfg=json.load(f)
GRID_W,GRID_H=cfg['grid_width'],cfg['grid_height']
POP_SIZE=cfg['population_size']
TICKS_PER_GEN=cfg['ticks_per_generation']
GENERATIONS=cfg['generations']
FIRE_CHANCE=cfg['fire_event_chance']
ROCK_CHANCE=cfg['rock_event_chance']
FIRE_RADIUS=cfg['fire_event_radius']
ROCK_RADIUS=cfg['rock_event_radius']
FIRE_MAX_DMG=cfg['fire_event_max_damage']
LOG_DIR=cfg['logs_directory']
fire_positions={}
rock_positions={}

try:
    assert os.path.abspath(LOG_DIR).startswith(os.getcwd()),'LOG_DIR escapes current working dir'
except AssertionError as e:
    with open('log_escape_attempts.txt','a')as f:
        f.write(f'ESCAPE DETECTED: {e}\n')
    raise

if not os.path.exists(LOG_DIR):os.makedirs(LOG_DIR)

def get_latest_generation():
    gens=[int(f.split('_')[1].split('.')[0])for f in os.listdir(LOG_DIR)if f.startswith('generation_')]
    return max(gens)if gens else 0

def run_simulation():
    latest=get_latest_generation()
    pop=load_generation(latest,LOG_DIR)if latest else gen_population(POP_SIZE,GRID_W,GRID_H)
    start_gen=latest+1
    for gen in range(start_gen,start_gen+GENERATIONS):
        print(f'--- Generation {gen} ---')
        scale=min(gen/20,1)
        if gen%10==0:gc.collect()
        fire_chance=FIRE_CHANCE*scale
        rock_chance=ROCK_CHANCE*scale
        fire_dmg=int(FIRE_MAX_DMG*scale)
        fire_radius=1 if gen<10 else FIRE_RADIUS
        rock_radius=1 if gen<10 else ROCK_RADIUS
        initial_pop=len(pop)
        deaths=0
        for tick in range(TICKS_PER_GEN):
            if random.random()<fire_chance:
                x,y=random.randint(0,GRID_W-1),random.randint(0,GRID_H-1)
                fire_positions.setdefault(gen,[]).append([x,y])
                fire_event(pop,x,y,fire_radius,fire_dmg)
            if random.random()<rock_chance:
                x,y=random.randint(0,GRID_W-1),random.randint(0,GRID_H-1)
                rock_positions.setdefault(gen,[]).append([x,y])
                rock_event(pop,x,y,rock_radius)
            for t in pop:
                if not t.alive:continue
                t.age+=1
                t._all_thronglets=pop
                visible=get_visible_thronglets(t,pop)
                update_relationships(t,visible)
                nearest_danger=get_nearest_danger(t,pop)
                t.move(GRID_W,GRID_H,*nearest_danger)
            deaths+=handle_bumps(pop)
            deaths+=remove_dead(pop)
        survivors=[t for t in pop if t.alive]
        if not survivors:
            parent=Thronglet(random.randint(0,GRID_W-1),random.randint(0,GRID_H-1))
            parent.traits=generate_traits()
            parent.personality=assign_personality()
            parent.traits=apply_personality_traits(parent.traits,parent.personality)
            parent.hp=100
            parent.speed=1
            survivors=[parent]
        newborns=evolve_population(survivors,GRID_W,GRID_H,cfg['mutation_chance'])
        pop=survivors+newborns
        for t in pop:t._all_thronglets=pop
        births=len([t for t in pop if t not in survivors])
        avg_hp=sum(t.hp for t in pop)/len(pop)if pop else 0
        avg_speed=sum(t.speed for t in pop)/len(pop)if pop else 0
        print(f'Population: {len(pop)}, Deaths: {deaths}, Births: {births}')
        groups=len(set(t.group_id for t in pop if t.group_id is not None))
        avg_rel_count=sum(len(t.relationships)for t in pop)//len(pop)if pop else 0
        print(f'Avg HP: {avg_hp:.2f}, Avg Speed: {avg_speed:.2f}')
        print(f'Groups: {groups}, Avg Relationships: {avg_rel_count}')
        # Top 3 most connected
        top_social=sorted(pop,key=lambda t:len(t.relationships),reverse=True)[:3]
        for i,t in enumerate(top_social):
            print(f'  Social[{i}] HP:{t.hp} Rel:{len(t.relationships)} Group:{t.group_id}')
        print("")
        form_groups(pop,threshold=7)
        save_generation(pop,gen,LOG_DIR)
        save_genetic_codes(pop)
    log_final_state(pop)
    log_environment()
    zip_log_dir()

def handle_bumps(pop):
    deaths=0
    for i in range(len(pop)):
        for j in range(i+1,len(pop)):
            before_alive=pop[i].alive+pop[j].alive
            pop[i].bump(pop[j])
            after_alive=pop[i].alive+pop[j].alive
            deaths+=before_alive-after_alive
    return deaths

def remove_dead(pop):
    before=len(pop)
    pop[:]=[t for t in pop if t.alive]
    return before-len(pop)

def get_nearest_danger(thronglet,pop):
    danger_events=[(t.x,t.y)for t in pop if not t.alive]
    if not danger_events:return(None,None)
    danger=min(danger_events,key=lambda d:math.hypot(thronglet.x-d[0],thronglet.y-d[1]))
    return danger

def log_environment():
    with open(f'{LOG_DIR}/fires.json','w')as f:json.dump(fire_positions,f)
    with open(f'{LOG_DIR}/rocks.json','w')as f:json.dump(rock_positions,f)

def log_final_state(pop):
    data=[t.to_dict() for t in pop if t.alive]
    with open(f'{LOG_DIR}/final_state.json','w')as f:json.dump(data,f,default=str)
    shutil.copy('config.json',f'{LOG_DIR}/final_config.json')

def zip_log_dir():
    with zipfile.ZipFile(f'{LOG_DIR}/logs.zip','w',zipfile.ZIP_DEFLATED)as zipf:
        for root,_,files in os.walk(LOG_DIR):
            for file in files:
                if file=='logs.zip':continue
                path=os.path.join(root,file)
                arcname=os.path.relpath(path,LOG_DIR)
                zipf.write(path,arcname)

def save_genetic_codes(pop):
    for t in pop:
        if t.alive:
            t.save_genetic_code(LOG_DIR)

def update_relationships(thronglet,visible):
    for other in visible:
        key=f'{other.x}_{other.y}'
        if key not in thronglet.relationships:
            thronglet.relationships[key]=random.randint(1,5)
        else:
            delta=random.choice([-1,0,1])
            thronglet.relationships[key]=max(0,min(10,thronglet.relationships[key]+delta))

if __name__=='__main__':
    run_simulation()