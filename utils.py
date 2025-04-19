import os,json,shutil

def list_generations():
    return sorted(f for f in os.listdir('logs')if f.startswith('generation_'))

def remove_generation(gen_num):
    f=f'logs/generation_{gen_num}.json'
    if os.path.exists(f):os.remove(f)

def reset_simulation():
    if os.path.exists('logs'):
        shutil.rmtree('logs')
    os.makedirs('logs')

def load_generation(gen_num):
    f=f'logs/generation_{gen_num}.json'
    if not os.path.exists(f):return[]
    with open(f,'r')as file:return json.load(file)

def analyze_generation(gen_num):
    data=load_generation(gen_num)
    if not data:return{}
    avg_hp=sum(t['hp']for t in data)/len(data)
    avg_speed=sum(t['speed']for t in data)/len(data)
    avg_detection=sum(t['detection_range']for t in data)/len(data)
    avg_avoidance=sum(t['avoidance_speed']for t in data)/len(data)
    analysis={
        'avg_hp':avg_hp,
        'avg_speed':avg_speed,
        'avg_detection_range':avg_detection,
        'avg_avoidance_speed':avg_avoidance,
        'total_alive':len(data)
    }
    return analysis

def save_analysis(gen_num):
    analysis=analyze_generation(gen_num)
    with open(f'logs/analysis_gen_{gen_num}.json','w')as file:
        json.dump(analysis,file)