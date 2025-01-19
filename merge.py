import json

target_date = "2025-01" # merge target month
days = ["04","05","17","18"]
result_list = []
for day in days:
    file_path = f"/home/bokjunsoo/testspark/data/{target_date}-{day}.json"
    with open(file_path, encoding = "UTF-8-SIG") as file:
            result_list.extend(json.load(file))

save_path = "/home/bokjunsoo/testspark/data/test_data.json"
with open(save_path, "w", encoding = "UTF-8-SIG") as f:
    json.dump(result_list
              ,f
              ,ensure_ascii=False
              ,indent='\t')