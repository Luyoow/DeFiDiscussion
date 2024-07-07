import json
from datetime import datetime
import hashlib


def parse_conversation(conversation):
    lines = conversation.strip().split('\n')
    parsed_conversation = []
    
    for line in lines:
        timestamp_str, rest = line.split('] <')
        user, message = rest.split('> ')
        timestamp = datetime.strptime(timestamp_str[1:], '%Y-%m-%d %H:%M:%S')
        parsed_conversation.append({"timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),"user": user,"body": message})
    
    return parsed_conversation


def generate_id_from_content(conversation):
    # 创建 SHA-256 哈希对象
    hash_object = hashlib.sha256()
    # 更新哈希对象，编码为 UTF-8 格式
    hash_object.update(conversation.encode('utf-8'))
    # 返回哈希值的十六进制表示
    return hash_object.hexdigest()


file_path = 'classification/data/origin_data_incident.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()


file_path = 'classification/data/data_incident.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.close()


# 分割对话
conversations = content.split('--------------------------------------------------------------------------------')
for i, conversation in enumerate(conversations):
    parsed_conversation = parse_conversation(conversation.strip())
    conversation_id = generate_id_from_content(conversation.strip())
    if 'incident' in file_path:
        label = "feature"
    else:
        label = "other"
    conversation_json = {"id": conversation_id, "body": "", "comments": parsed_conversation, "label": label}
    conversation_json_str = json.dumps(conversation_json, indent=4)
    conversation_json_str = conversation_json_str.replace('\n', '').replace('    ', '')
    
    with open('classification/data/data_incident.txt', 'a', encoding='utf-8') as output_file:
       output_file.write(conversation_json_str)
       output_file.write('\n')
       
       


file_path = 'classification/data/origin_data_normal.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
    

file_path = 'classification/data/data_normal.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.close()

# 分割对话
conversations = content.split('--------------------------------------------------------------------------------')
for i, conversation in enumerate(conversations):
    parsed_conversation = parse_conversation(conversation.strip())
    conversation_id = generate_id_from_content(conversation.strip())
    if 'incident' in file_path:
        label = "feature"
    else:
        label = "other"
    conversation_json = {"id": conversation_id, "body": "", "comments": parsed_conversation, "label": label}
    conversation_json_str = json.dumps(conversation_json, indent=4)
    conversation_json_str = conversation_json_str.replace('\n', '').replace('    ', '')
    
    with open('classification/data/data_normal.txt', 'a', encoding='utf-8') as output_file:
       output_file.write(conversation_json_str)
       output_file.write('\n')