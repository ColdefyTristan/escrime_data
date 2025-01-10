"""This script is used to count the types of rejection of a rejection_result file"""


import json
from collections import Counter

json_file = "rejection_results_2024-12-11_11-27-28.json"

with open(json_file, "r") as file:
    data = json.load(file)

false_count = sum(1 for item in data.values() if not item.get("result", True))

reason_counter = Counter(item.get("reason") for item in data.values() if "reason" in item)

print(f"Nombre de 'false' dans 'result': {false_count}")
print("Occurrences des 'reason':")
for reason, count in reason_counter.items():
    print(f"  {reason}: {count}")
