import sys
import json 
import pandas as pd
from datetime import datetime

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        convo_list = json.load(f)
        df_array = []

        for convo in convo_list:
            create_time = convert_unix_time_to_readable(convo["create_time"])
            update_time = convert_unix_time_to_readable(convo["update_time"])
            
            #parse conversation history to dataFrame
            message_list = convo["mapping"]
            data_to_insert = [] 
            
            for uuid, info in message_list.items():
                message = info.get("message")                
                if(message is not None): 
                    data_to_insert.append({
                        "conversation_id": convo["conversation_id"],
                        "title": convo["title"],
                        "created_at": create_time,
                        "updated_at": update_time,
                        "message_id": uuid,
                        "message_created_at": convert_unix_time_to_readable(message.get("create_time")),
                        "author": message.get("author", {}).get("role"),
                        "part": message.get("content", {}).get("parts")
                    })
            
            df = pd.DataFrame(data_to_insert)
            df_array.append(df)
                
        #export to csv file
        combined_df = pd.concat(df_array, ignore_index=True)
        combined_df.to_csv('chatgpt_parsed_chat_log.csv', index=False)
     
#convert unix time to readable time              
def convert_unix_time_to_readable(unix_time):
    if (unix_time is not None):
        target_time = datetime.fromtimestamp(unix_time)
        dt_format_str = '%Y-%m-%d %H:%M:%S'
        return target_time.strftime(dt_format_str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_data.py </path/to/conversations.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
    