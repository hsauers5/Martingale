import requests
import json

count = 0
average_return = 0
geomean_return = 1
average_times_to_win = 0

for i in range(0, 100):
  count += 1
  response = requests.get('https://martingaleapi.harrysauers.repl.co/calculate?odds=0.5').content

  stats = json.loads(response, encoding='UTF-8')
  average_return += float(stats['return'])
  geomean_return *= 1 + float(stats['return'])

  average_times_to_win += int(stats['count'])

average_return /= count
average_times_to_win /= count
geomean_return -= 1

print('Average times to win: ' + str(average_times_to_win))
print('Average return: ' + str(average_return))
print('Average geomean return: ' + str(geomean_return))
