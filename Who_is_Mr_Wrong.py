import json
import re
conversation=[
"Frodo:I'm in 3rd position.",
      "Gollum:I'm in 3rd position.",
      "Sam:The man behind me is Frodo.",
      "Gollum:The man behind me is Frodo."
]
class MrWrong:
    def __init__(self, list_str_data):
        base_data_str = self.get_data_for_list_str(list_str_data)
        base_list_name = list(base_data_str.keys())
        len_base_list_name = len(base_list_name)
        self.base_dict_name = {}
        self.mr_wrong_list = []
        self.mr_wrong_list_potential = []
        for name, data_name_list in base_data_str.items():
            assert_data_one_person = self.get_rule_for_str_list_and_assert(data_name_list,
                                                                           len_base_list_name, name)
            self.base_dict_name.update({name: assert_data_one_person})



    def get_decomposition(self, queue_length,  data_in,position_decompose ={}, assert_position=0):
        position_front = 0
        position_behind = 0
        for name, rule_for_name in data_in.items():
            position = rule_for_name.get("position")
            name_front = rule_for_name.get("front", [0])[0]
            name_behind = rule_for_name.get("behind", [0])[0]
            if position:
                position = position[0]
                condition_1 = [True if (position <= 0 and position > queue_length) else False]
                # вверх и вниз ссылается на одного и того же
                condition_2 = [True if (assert_position and assert_position != position) else False]
                if any(condition_1+condition_2):
                    break
                if position not in position_decompose.keys():
                    position_decompose.update({position: name})
                    position_front = position - 1
                    position_behind = position + 1
            if name_front:
                data_front = {name_front:rule_for_name_front for name_front, rule_for_name_front
                              in data_in.items() if name_front != name}
                res_front = self.get_decomposition(queue_length, data_front, position_decompose=position_decompose,
                                                   assert_position=position_front)
                position_decompose.update(res_front)
            if name_behind:
                data_behind = {name_behind:rule_for_name_behind for name_behind, rule_for_name_behind
                              in data_in.items() if name_behind != name}
                res_behind = self.get_decomposition(queue_length, data_behind, position_decompose=position_decompose,
                                                    assert_position=position_behind)
                position_decompose.update(res_behind)

        return position_decompose



    @staticmethod
    def get_data_for_list_str(list_str):
        dict_rule_txt_for_name = {}
        for rule_str in list_str:
            conversation_list = rule_str.split(":")
            name, rule_txt = conversation_list
            if dict_rule_txt_for_name.get(name):
                dict_rule_txt_for_name[name].append(rule_txt)
            else:
                dict_rule_txt_for_name[name] = [rule_txt]
        return dict_rule_txt_for_name

    def assert_condition_one_person(self, dict_assert, name):
        # человек ссылается сам на себя или дважды говорит об одном и том же разное
        condition_1 = [True if val[0] == name or len(val) > 1 else False for key, val in dict_assert.items()]
        # вверх и вниз ссылается на одного и того же
        condition_2 = [dict_assert.get("behind", 1) == dict_assert.get("front", 2)]
        rule_assert_mr_wrong = condition_1 + condition_2
        if any(rule_assert_mr_wrong):
            self.mr_wrong_list.append(name)
    def get_rule_for_str_list_and_assert(self, str_rule_list, queue_length, name):
        dict_out = {}
        for str_rule in str_rule_list:
            int_str = re.findall(r'\d+', str_rule)
            value_params, key_params = '', ''
            if int_str:
                value_params = int(int_str[0])
                key_params = "position"
                if "people in front of me" in str_rule:
                    value_params += 1
                elif "people behind me." in str_rule:
                    value_params = queue_length - value_params
            else:
                if "The man behind me is" in str_rule:
                    value_params = str_rule.split("The man behind me is ")[1][:-1]
                    key_params = "behind"
                elif "The man in front of me is " in str_rule:
                    value_params = str_rule.split("The man in front of me is ")[1][:-1]
                    key_params = "front"
            cur_params = dict_out.get(key_params)
            if cur_params:
                dict_out[key_params] = cur_params + [value_params]
            else:
                dict_out.update({key_params: [value_params]})
        self.assert_condition_one_person(dict_out, name)
        return dict_out
import json
def find_out_mr_wrong(conversation):
    mr_wrong = MrWrong(conversation)
    base_data = mr_wrong.base_dict_name
    len_base_data = len(base_data.keys())
    print(mr_wrong.get_decomposition(len_base_data, base_data))
    print(json.dumps(base_data, indent=2))
print(find_out_mr_wrong(conversation))



