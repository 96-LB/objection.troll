def merge(data):
    out = {
        'type': 'scene',
        'options': {
            'chatbox': 0,
            'textSpeed': 30,
            'textBlipFrequency': 64,
            'autoplaySpeed': 750,
            'continueSoundUrl': ''
        },
        'groups': [
            {
                'iid': 1,
                'name': 'Main',
                'type': 'n',
                'frames': []
            }
        ],
        'courtRecord': {
            'evidence': [],
            'profiles': []
        },
        'aliases': [],
        'pairs': [],
        'version': 4
    }
    
    out_frames = out['groups'][0]['frames']
    out_aliases = out['aliases']
    out_pairs = out['pairs']
    
    # merge files
    pair_id = 1
    for datum in data:
        
        version = datum['version']
        if version == 3:
            frames = datum['frames']
            pairs = datum['pairs']
            aliases = datum['aliases']
        elif version == 4:
            frames = datum['groups'][0]['frames']
            pairs = datum['pairs']
            aliases = datum['aliases']
        else:
            continue
        
        pair_map = {}
        for pair in pairs:
            pair_map[pair['pairId']] = pair_id
            pair['pairId'] = pair_id
            pair_id += 1
            
        if pair_map:
            for frame in frames:
                if frame['pairId'] in pair_map:
                    frame['pairId'] = pair_map[frame['pairId']]
        
        out_frames += frames
        out_pairs += pairs

    return out
