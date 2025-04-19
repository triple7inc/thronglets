import random,math
def form_groups(pop,threshold=7):
    group_id=0
    assigned=set()
    for t in pop:
        if t in assigned:continue
        group=[t]
        for key,score in t.relationships.items():
            if score>=threshold:
                x,y=map(lambda v:int(float(v)),key.split('_'))
                match=[o for o in pop if o.x==x and o.y==y and o.alive]
                if match:group.append(match[0])
        for member in group:
            member.group_id=group_id
            assigned.add(member)
        group_id+=1

def update_relationships(pop):
    for t in pop:
        for other in pop:
            if t==other:continue
            distance=math.hypot(t.x-other.x,t.y-other.y)
            if distance<=t.detection_range:
                t.relationships[f'{other.x}_{other.y}']=t.traits['charisma']-distance//2
                other.relationships[f'{t.x}_{t.y}']=other.traits['charisma']-distance//2

def merge_groups(pop,threshold=10):
    group_dict={}
    for t in pop:
        group_id=t.group_id
        if group_id not in group_dict:
            group_dict[group_id]=[]
        group_dict[group_id].append(t)

    for group in group_dict.values():
        if len(group)>1:
            avg_relation=sum([sum(t.relationships.values()) for t in group])/len(group)
            if avg_relation>=threshold:
                new_group_id=group[0].group_id
                for member in group:
                    member.group_id=new_group_id

def print_group_details(pop):
    groups={}
    for t in pop:
        if t.group_id not in groups:
            groups[t.group_id]=[]
        groups[t.group_id].append(t)

    for group_id,members in groups.items():
        print(f"Group {group_id}:")
        for member in members:
            print(f"  - HP: {member.hp}, Speed: {member.speed}, Relationships: {member.relationships}")