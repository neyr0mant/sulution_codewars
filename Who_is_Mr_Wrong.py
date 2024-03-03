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

conversation6=[
"John:I'm in 1st position.",
"Peter:I'm in 2nd position.",
"Tom:I'm in 1st position.",
]
list_conversation = [conversation1, conversation2,conversation3,conversation4, conversation5, conversation6]
# lsit_acssert = [1,2,3,4,5,6]
lsit_acssert = [1,2,3,4,5,6]
list_conversation = [i for idx, i in enumerate(list_conversation) if idx in lsit_acssert]
import re
import json

def get_data_for_list_str(list_str):
    dict_rule_txt_for_name = {}
    for rule_str in list_str:
        conversation_list = rule_str.split(":")
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
    return data_for_name

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


def use_rule_and_assert_composition(data_in, rule):
    print()


def get_data_position_rule_and_assert(data_in):
    len_names = len(data_in.keys())
    name_with_position = {}
    name_not_position = {}
    potential_mr_wrong = []
    potential_mr_right = []
    for idx, data_name in enumerate(data_in.items()):
        name, data = data_name
        position = data.get("position")
        potential_mr_right.append(name)
        if position:
            exist_name = name_with_position.get(position)
            if exist_name:
                name_add = exist_name + [name]
                name_with_position[position] = name_add
                potential_mr_wrong.extend(name_add)
                del potential_mr_right[idx]

            else:
                name_with_position[position] = [name]
        else:
            name_not_position.update({name: data})
    position_found = list(name_with_position.keys())

    assert_rule = any([len(position_found) == len_names, # условие если всех распределили по позициям
                       len(potential_mr_wrong) > 2, # услови если лжецов больше 2
                       len(potential_mr_right) + len(potential_mr_wrong) >
                       len_names and not name_not_position # условие если нет людей без позиции,
                       # но при этом количесрво потенциных лжецов и правдивых равно длине списка
                       ])
    return assert_rule, name_with_position, name_not_position, potential_mr_wrong


def find_out_mr_wrong(conversation):
    data_for_name = get_data_for_list_str(conversation)
    assert_composition, name_with_position, name_not_position, potential_mr_wrong = (
        get_data_position_rule_and_assert(data_for_name))
    if assert_composition:
        print("РЕШЕНИЙ НЕТ! ")
        return None
    print("РЕШЕНИЯ ЕСТЬ! ")
    # print(json.dumps(data_for_name, indent=2))
    # print(json.dumps(name_with_position, indent=2))
    # print(json.dumps(name_not_position, indent=2))




for idx, conversation in enumerate(list_conversation):
    print(f"НАБОР НОМЕР {idx+1}")
    print(find_out_mr_wrong(conversation))




