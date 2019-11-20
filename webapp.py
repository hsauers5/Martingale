from flask import Flask, request, jsonify, abort
import requests

app = Flask('s')

@app.route('/', methods=['GET'])
def home():
 return 'Hello World. '


@app.route('/calculate', methods=['GET'])
def calculate():
  odds = request.args['odds']
  if 'bet' in request.args.keys():
    try:
      bet = float(request.args['bet'])
    except ValueError:
      abort(400)
  else:
    bet = 1
  
  try:
    odds = float(odds)
  except ValueError:
    abort(400)

  if odds > 1:
    abort(400)

  stats = martingale(odds, initial_bet_size=bet)

  return jsonify(stats)


def martingale(odds, initial_bet_size=1):
  count = 0
  bet_size = initial_bet_size

  money = 0

  while True:
    count += 1
    bet_size *= 2

    # get a true random number
    random_number = int(requests.get('https://www.random.org/integers/?num=1&min=1&max=100&col=1&base=10&format=plain&rnd=new').content)

    # win or lose?
    threshold = odds * 100
    if random_number< threshold:
      print('You win!')
      money += bet_size
      break
    else:
      print('You lose!')
      money -= bet_size

  # impute % return on max risk
  return_on_max_risk = money / bet_size

  # print stats
  print('# of times to win: ' + str(count))
  print('End-Money: ' + str(money))
  print('End bet size: ' + str(bet_size))
  print('Return on max risk: ' + str(return_on_max_risk))

  # return dict
  return {'count': count, 'balance': money, 'return': return_on_max_risk}


app.run(debug=False, host='0.0.0.0')
print('API is live. ')
