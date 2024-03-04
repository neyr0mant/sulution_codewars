conversation1=[
"Tom:I'm in 2nd position.",
"Peter:The man behind me is Tom.",
"John:The man behind me is Tom."
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
conversation5 = [
    'Mnulesil:The man in front of me is Reoowpqgn.',
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
 'Aiaug:There are 7 people behind me.'
]

conversation6=[
"John:I'm in 1st position.",
"Peter:I'm in 2nd position.",
"Tom:I'm in 1st position.",
]
conversation7 = ["Tom:The man behind me is Bob.",
      "Bob:The man in front of me is Tom.",
      "Bob:The man behind me is Gary.",
      "Gary:The man in front of me is Bob.",
      "Fred:I'm in 1st position."]
list_conversation = [conversation1, conversation2,conversation3,conversation4, conversation5, conversation6, conversation7]
# lsit_acssert = [0,1, 2,3,4,5,6]
lsit_acssert = [0]
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
    all_name = set(dict_rule_txt_for_name.keys())
    len_set_name = len(all_name)
    all_position = {i for i in range(1, len_set_name+1)}
    data_for_name = {}
    mr_wrong = False
    list_name_same_position = []
    data_position = {}
    data_link_name = {}
    position_find = set()
    position_for_name = {}
    plus_minus_data = {}
    for name, list_data in dict_rule_txt_for_name.items():
        for data_str in list_data:
            cur_params = data_for_name.get(name, {})
            key_params, value_params = get_params_str(data_str, len_set_name)
            if key_params in ["position_plus", "position_minus"]:
                if value_params == name: # когда человек ссылается сам на себя - значит он врун
                    mr_wrong = name
                    break
                list_name_position_plus_minus = plus_minus_data.get(key_params)
                if list_name_position_plus_minus:
                    name_plus_minus = list_name_position_plus_minus[0]
                    if data_link_name[name_plus_minus].get(key_params) == value_params:
                        list_name_same_position.extend([name, name_plus_minus])
                        #два человека ссылаются на одного и того идя вверх или низ - значит среди них врун
                else:
                    plus_minus_data[key_params] = [name]
            if isinstance(value_params, int):
                data_position.update({name: {key_params: value_params}})
                exist_position = position_for_name.get(value_params)
                position_for_name.update({value_params:[name]})
                if value_params in position_find:
                    if exist_position:
                        new_mr_wrong_list = exist_position + [name]
                        if position_for_name.get(value_params):
                            list_name_same_position = new_mr_wrong_list
                position_find.add(value_params)
            else:
                data_link_name.update({name: {key_params: value_params}})
            cur_params.update({key_params: value_params})
            data_for_name.update({name:cur_params})
        if mr_wrong:
            break
    position_free = all_position- position_find
    return data_position, data_link_name, mr_wrong, list_name_same_position, all_name, position_free, all_position

def get_params_str(str_in, queue_length):
    int_str = re.findall(r'\d+', str_in)
    value_params, key_params = '', ''
    if int_str:
        value_params = int(int_str[0])
        key_params = "position"
        if "people in front of me" in str_in:
            value_params += 1
        elif "people behind me." in str_in:
            value_params = queue_length - value_params
    else:
        if "The man behind me is" in str_in:
            value_params = str_in.split("The man behind me is ")[1][:-1]
            key_params = "position_plus"
        elif "The man in front of me is " in str_in:
            value_params = str_in.split("The man in front of me is ")[1][:-1]
            key_params = "position_minus"
    return key_params,value_params

def get_exist_position(data_in):
    exist_position = []
    for name, position_data in data_in.items():
        exist_position.append(position_data["position"])
    return set([i["position"] for i in data_in.values()])


get_exist_position({'John': {'position': 1}, 'Peter': {'position': 2}, 'Tom': {'position': 1}})
print()
def assert_position_rule(data_position, data_link, position_free, all_position, name_assert):
    for name, data in data_link.items():
        list_name_neighbour = [data.get("position_plus"), data.get("position_minus")]
        for idx, name_neighbour in enumerate(list_name_neighbour):
            if name_neighbour == name_assert:
                plus = -1 if idx == 0 else 1
                print()



def find_out_mr_wrong(conversation):
    data_position, data_link_name, mr_wrong, list_name_same_position, all_name, position_free, all_position = (
        get_data_for_list_str(conversation))
    if mr_wrong:
        return mr_wrong
    if list_name_same_position:
        for name_same_position in list_name_same_position:
            res = assert_position_rule(data_position, data_link_name, position_free, all_position,
                                       name_same_position)


    # print(assert_composition)
    # print(f"Имена без позиций: {name_not_position}")
    # print(f"Имена с позициями: {name_with_position}")
    # print()

for idx, conversation in enumerate(list_conversation):
    print(f"НАБОР НОМЕР {idx+1}")
    print(find_out_mr_wrong(conversation))



