conversation1=[
"John:I'm in 1st position.",
"Peter:I'm in 2nd position.",
"Tom:I'm in 1st position.",
"Peter:The man behind me is Tom."
]

conversation2=[
"John:I'm in 1st position.",
"Peter:I'm in 2nd position.",
"Tom:I'm in 1st position.",
"Peter:The man in front of me is Tom."
]

conversation3=[
"John:I'm in 1st position.",
"Peter:There is 1 people in front of me.",
"Tom:There are 2 people behind me.",
"Peter:The man behind me is Tom."
]

conversation4=[
"John:The man behind me is Peter.",
"Peter:There is 1 people in front of me.",
"Tom:There are 2 people behind me.",
"Peter:The man behind me is Tom."
]
conversation5 = ['Mnulesil:The man in front of me is Reoowpqgn.',
 'Sene:There are 6 people in front of me.',
 "Qqeod:I'm in 6th position.",
 'Gdimeia:There are 9 people behind me.',
 'Hekoo:There are 2 people behind me.',
 'Aiaug:The man behind me is Reoowpqgn.',
 'Reoowpqgn:There are 6 people behind me.',
 'Gdimeia:There are 0 people in front of me.',
 'Qqeod:The man in front of me is Mnulesil.',
 'Hekoo:There are 7 people in front of me.',
 'Rynuk:The man behind me is Rynuk.',
 "Yemeyai:I'm in 2nd position.",
 'Ooseebb:The man in front of me is Hekoo.',
 'Reoowpqgn:There are 3 people in front of me.',
 'Mnulesil:There are 5 people behind me.',
 "Rynuk:I'm in 9th position.",
 'Aiaug:There are 7 people behind me.']
list_conversation = [conversation1, conversation2,conversation3,conversation4, conversation5]
list_conversation = [i for idx, i in enumerate(list_conversation) if idx in [1]]
import re
import json
def get_params_str(str_in, queue_length):
    find_int = re.findall(r'\d+', str_in)
    value_params, key_params = '', ''
    if find_int:
        value_params = int(find_int[0])
        key_params = "position"
        if "people in front of me" in str_in:
            value_params += 1
        elif "people behind me." in str_in:
            value_params = queue_length - value_params
    else:
        if "The man behind me is" in str_in:
            value_params = str_in.split("The man behind me is ")[1][:-1]
            key_params = "position_plus_name"
        elif "The man in front of me is " in str_in:
            value_params = str_in.split("The man in front of me is ")[1][:-1]
            key_params = "position_minus_name"
    return {key_params: value_params}


def assert_composition_rule(data_in):
    len_names = len(data_in.keys())
    all_position = set([i for i in range(1, len_names+1)])
    position_for_name = {}
    name_not_position = {}
    list_name_mr_wrong = []
    for name, data in data_in.items():
        position = data.get("position")
        if position:
            exist_name = position_for_name.get(position)
            if exist_name:
                list_name_mr_wrong.extend([name, exist_name])
            else:
                position_for_name.update({position: name})
        else:
            name_not_position.update({name: data})
    position_found = set(list(position_for_name.keys()))
    if len(position_found) == len_names:
        return True, position_for_name
    position_free = all_position - position_found
    while position_found != all_position:
        for not_position, data_no_position in name_not_position.items():
            rule_no_position, name_ = list(data_no_position.items())[0]
            print()
    return (True, position_for_name) if len(position_for_name.keys()) == len_names else (False, list_name_mr_wrong)

def find_out_mr_wrong(conversation):
    dict_rule_txt_for_name = {}
    for conversation_ in conversation:
        conversation_list = conversation_.split(":")
        name, rule_txt = conversation_list
        if dict_rule_txt_for_name.get(name):
            dict_rule_txt_for_name[name].append(rule_txt)
        else:
            dict_rule_txt_for_name[name] = [rule_txt]
    set_name = set(dict_rule_txt_for_name.keys())
    len_set_name = len(set_name)
    data_for_name = {}
    for name, list_data in dict_rule_txt_for_name.items():
        for data_str in list_data:
            data_for_name.update({name: get_params_str(data_str, len_set_name)})
    exist_composition, list_name_mr_wrong = assert_composition_rule(data_for_name)
    if exist_composition:
        return None
    data_mr_right = {name:data_name for name, data_name in data_for_name.items() if name not in list_name_mr_wrong}
    data_mr_wrong = {name:data_name for name, data_name in data_for_name.items() if name in list_name_mr_wrong}
    not_key_err = False
    for mr_wrong in list_name_mr_wrong:
        data_mr_right.update({mr_wrong:data_for_name[mr_wrong]})
        res_assert, type_not_composition = assert_composition_rule(data_mr_right)
        if not_key_err and res_assert:
            print()
        del data_mr_right[mr_wrong]
        not_key_err = True if type_not_composition == "not_key" else not_key_err


for idx, conversation in enumerate(list_conversation):
    print(f"НАБОР НОМЕР {idx+1}")
    print(find_out_mr_wrong(conversation))




