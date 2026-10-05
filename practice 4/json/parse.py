import json
with open('sample-data.json') as f:
    d = json.load(f)
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
print("-" * 50, "-" * 20, "-" * 10, "-" * 6)
for i in d['imdata']:
    a = i['l1PhysIf']['attributes']
    print(f"{a['dn']:<50} {a['descr']:<20} {a['speed']:<10} {a['mtu']}")