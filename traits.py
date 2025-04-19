import random

TRAIT_NAMES=['strength','agility','awareness','resilience','fertility']

PERSONALITIES={
    'aggressive':{'strength':1,'agility':0,'awareness':-1,'resilience':0,'fertility':0},
    'timid':{'strength':-1,'agility':1,'awareness':1,'resilience':0,'fertility':0},
    'curious':{'strength':0,'agility':1,'awareness':1,'resilience':-1,'fertility':0},
    'selfish':{'strength':0,'agility':0,'awareness':0,'resilience':0,'fertility':1},
    'protective':{'strength':1,'agility':0,'awareness':1,'resilience':1,'fertility':-1}
}

def generate_traits(base=None,mutation_chance=0.1):
    traits={k:(base[k]if base else random.randint(1,3))for k in TRAIT_NAMES}
    for k in traits:
        if random.random()<mutation_chance:
            traits[k]+=random.choice([-1,1])
        if random.random()<0.05:
            traits[k]-=1
        traits[k]=max(1,min(traits[k],10))
    return traits

def assign_personality():
    return random.choice(list(PERSONALITIES.keys()))

def apply_personality_traits(traits,personality):
    if personality in PERSONALITIES:
        mods=PERSONALITIES[personality]
        for k in traits:
            traits[k]+=mods.get(k,0)
            traits[k]=max(1,min(traits[k],10))
    return traits