import gambit

def build_reset_game(array, reset_probability_array):
    admin_email = array[0]
    admin_bomb = array[1]
    admin_escalate = array[2]
    a_reset = array[3]
    user_email = array[4]
    user_bomb = array[5]
    user_escalate = array[6]
    u_reset = array[7]

    g = gambit.Game.new_tree()
    g.title = "Reset Game"

    l = g.players.add("Admin")
    f = g.players.add("User")

    move = g.root.append_move(g.players.chance, 2)
    move.actions[0].label = "Successful reset"
    move.actions[0].prob = reset_probability_array[0]
    move.actions[1].label = "Reset failure"
    move.actions[1].prob = 1-reset_probability_array[0]
    

    reset_works = g.outcomes.add()
    reset_works[0] = a_reset
    reset_works[1] = u_reset
    g.root.children[0].outcome = reset_works

    move = g.root.children[1].append_move(f, 3)
    move.actions[0].label = "Email admin"
    move.actions[1].label = "Email bomb admin"
    move.actions[2].label = "Escalate"

    move = g.root.children[1].children[0].append_move(g.players.chance, 2)
    move.actions[0].label = "Successful reset"
    move.actions[0].prob = reset_probability_array[1]
    move.actions[1].label = "Reset failure"
    move.actions[1].prob = 1 - reset_probability_array[1]

    reset_email = g.outcomes.add()
    reset_email[0] = admin_email + a_reset
    reset_email[1] = user_email + u_reset
    g.root.children[1].children[0].children[0].outcome = reset_email

    move = g.root.children[1].children[0].children[1].append_move(f, 2)
    move.actions[0].label = "Email bomb admin"
    move.actions[1].label = "Escalate"

    email_escalate = g.outcomes.add()
    email_escalate[0] = admin_email + admin_escalate
    email_escalate[1] = user_email + user_escalate
    g.root.children[1].children[0].children[1].children[1].outcome = email_escalate

    move = g.root.children[1].children[0].children[1].children[0].append_move(g.players.chance, 2)
    move.actions[0].label = "Successful reset"
    move.actions[0].prob = reset_probability_array[2]
    move.actions[1].label = "Reset failure"
    move.actions[1].prob = 1 - reset_probability_array[2]

    reset_email_bomb = g.outcomes.add()
    reset_email_bomb[0] = admin_email + admin_bomb + a_reset
    reset_email_bomb[1] = user_email + user_bomb + u_reset
    g.root.children[1].children[0].children[1].children[0].children[0].outcome = reset_email_bomb

    email_bomb_escalate = g.outcomes.add()
    email_bomb_escalate[0] = admin_email + admin_bomb + admin_escalate
    email_bomb_escalate[1] = user_email + user_bomb + user_escalate
    g.root.children[1].children[0].children[1].children[0].children[1].outcome = email_bomb_escalate

    move = g.root.children[1].children[1].append_move(g.players.chance, 2)
    move.actions[0].label = "Successful reset"
    move.actions[0].prob = reset_probability_array[2]
    move.actions[1].label = "Reset failure"
    move.actions[1].prob = 1 - reset_probability_array[2]

    reset_bomb = g.outcomes.add()
    reset_bomb[0] = admin_bomb + a_reset
    reset_bomb[1] = user_bomb + u_reset
    g.root.children[1].children[1].children[0].outcome = reset_bomb

    bomb_escalate = g.outcomes.add()
    bomb_escalate[0] = admin_bomb + admin_escalate
    bomb_escalate[1] = user_bomb + user_escalate
    g.root.children[1].children[1].children[1].outcome = bomb_escalate

    escalate = g.outcomes.add()
    escalate[0] = admin_escalate
    escalate[1] = user_escalate
    g.root.children[1].children[2].outcome = escalate

    return g

def resetNash(g):
    solver = gambit.nash.ExternalLogitSolver()
    x = solver.solve(g)
    return x

def createResetFile(g):
    game = g.write(format='native')
    f = open("Reset.efg","w+")
    f.write(game)
    f.close()

def resetAdminPayoff(x, g):
    return x[0].payoff(g.players[0])

def resetUserPayoff(x, g):
    return x[0].payoff(g.players[1])

def build_big_game(user_endowment, cost_array, a, u, probability_array):
    admin_data_breach = -10 -1 * user_endowment
    user_data_breach = -2 * user_endowment
    perfect_run = 0

    pp1_login = cost_array[0]
    pp2_login_pi1 = cost_array[1]
    pp2_login = cost_array[2]

    admin_reset = a
    user_reset = u

    g = gambit.Game.new_tree()

    g.title = "Basic Game"
    l = g.players.add("Admin")
    f = g.players.add("User")

    move = g.root.append_move(l, 2)
    move.label = 'f'
    move.actions[0].label = "PP-1"
    move.actions[1].label = "PP-2"

    move = g.root.children[0].append_move(f, 2)
    move.label = 'a'
    move.actions[0].label = "PI-1"
    move.actions[1].label = "PI-2"

    move = g.root.children[1].append_move(f, 2)
    move.label = 'k'
    move.actions[0].label = "PI-1"
    move.actions[1].label = "PI-2"

    move = g.root.children[0].children[0].append_move(g.players.chance, 3)
    move.actions[0].label = "NOP"
    move.actions[0].prob = probability_array[0]
    move.actions[1].label = "F"
    move.actions[1].prob = probability_array[1]
    move.actions[2].label = "B"
    move.actions[2].prob = probability_array[2]

    g.root.children[1].children[0].append_move(move)

    move = move = g.root.children[0].children[1].append_move(g.players.chance, 3)
    move.actions[0].label = "NOP"
    move.actions[0].prob = probability_array[3]
    move.actions[1].label = "F"
    move.actions[1].prob = probability_array[4]
    move.actions[2].label = "B"
    move.actions[2].prob = probability_array[5]

    g.root.children[1].children[1].append_move(move)

    pp1_pi1_nop = g.outcomes.add()
    pp1_pi1_nop[0] = perfect_run
    pp1_pi1_nop[1] = pp1_login

    pp1_pi1_f = g.outcomes.add()
    pp1_pi1_f[0] = admin_reset
    pp1_pi1_f[1] = user_reset + pp1_login

    pp1_pi1_b = g.outcomes.add()
    pp1_pi1_b[0] = admin_data_breach
    pp1_pi1_b[1] = user_data_breach + pp1_login

    pp1_pi2_nop = g.outcomes.add()
    pp1_pi2_nop[0] = perfect_run
    pp1_pi2_nop[1] = pp2_login

    pp1_pi2_f = g.outcomes.add()
    pp1_pi2_f[0] = admin_reset
    pp1_pi2_f[1] = user_reset + pp2_login

    pp1_pi2_b = g.outcomes.add()
    pp1_pi2_b[0] = admin_data_breach
    pp1_pi2_b[1] = user_data_breach + pp2_login

    pp2_pi1_nop = g.outcomes.add()
    pp2_pi1_nop[0] = perfect_run
    pp2_pi1_nop[1] = pp2_login_pi1

    pp2_pi1_f = g.outcomes.add()
    pp2_pi1_f[0] = admin_reset
    pp2_pi1_f[1] = user_reset + pp2_login_pi1

    pp2_pi1_b = g.outcomes.add()
    pp2_pi1_b[0] = admin_data_breach
    pp2_pi1_b[1] = user_data_breach + pp2_login_pi1

    pp2_pi2_nop = g.outcomes.add()
    pp2_pi2_nop[0] = perfect_run
    pp2_pi2_nop[1] = pp2_login

    pp2_pi2_f = g.outcomes.add()
    pp2_pi2_f[0] = admin_reset
    pp2_pi2_f[1] = user_reset + pp2_login

    pp2_pi2_b = g.outcomes.add()
    pp2_pi2_b[0] = admin_data_breach
    pp2_pi2_b[1] = user_data_breach + pp2_login

    g.root.children[0].children[0].children[0].outcome = pp1_pi1_nop
    g.root.children[0].children[0].children[1].outcome = pp1_pi1_f
    g.root.children[0].children[0].children[2].outcome = pp1_pi1_b

    g.root.children[0].children[1].children[0].outcome = pp1_pi2_nop
    g.root.children[0].children[1].children[1].outcome = pp1_pi2_f
    g.root.children[0].children[1].children[2].outcome = pp1_pi2_b


    g.root.children[1].children[0].children[0].outcome = pp2_pi1_nop
    g.root.children[1].children[0].children[1].outcome = pp2_pi1_f
    g.root.children[1].children[0].children[2].outcome = pp2_pi1_b

    g.root.children[1].children[1].children[0].outcome = pp2_pi2_nop
    g.root.children[1].children[1].children[1].outcome = pp2_pi2_f
    g.root.children[1].children[1].children[2].outcome = pp2_pi2_b

    return g

def solve(g):
    solver = gambit.nash.ExternalLogitSolver()
    x = solver.solve(g)
    return x

def createFile(g):
    game = g.write(format='native')
    f = open("maingame.efg","w+")
    f.write(game)
    f.close()

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return int(num)-1

def payoff(x, g):
    y = x[0].payoff(g.players[0])   
    z = x[0].payoff(g.players[1])
    return (y,z)

def one_round(reset_costs, user_endowment, cost_array, probability_array, reset_probability_array = None):

    if reset_probability_array is None:
        reset_probability_array = [gambit.Rational(95,100), gambit.Rational(90,100), gambit.Rational(95,100)]
    
    g = build_reset_game(reset_costs, reset_probability_array)
    a = solve(g)
    createResetFile(g)

    admin_reset_payoff = resetAdminPayoff(a, g)

    admin_reset_payoff = gambit.Rational(formatNumber(admin_reset_payoff*100000),100000)
    user_reset_payoff = resetUserPayoff(a, g)
    user_reset_payoff = gambit.Rational(formatNumber(user_reset_payoff*100000),100000)

    g = build_big_game(user_endowment, cost_array, admin_reset_payoff, user_reset_payoff, probability_array)

    x = solve(g)
    createFile(g)
    (a,b) = payoff(x,g)
    return (a, b, x)

# Mehanism design to compare two policies with different probabilities and costs
def mech_design_compare_policies(reset_costs, user_endowment, cost_arrays, prob_arrays, reset_probability_array):
    results = []
    best_index = -1
    max_payoffs = -100000
    if len(cost_arrays) == len(prob_arrays):
        for i in range(len(cost_arrays)):
            (a, b, x) = one_round(reset_costs, user_endowment, cost_arrays[i], prob_arrays[i], reset_probability_array)
            results.append([(a, b), a + b, x])
            if (max_payoffs < (a+b)):
                max_payoffs = a + b
                best_index = i
    return results, best_index 

# Mehanism design to compare a single policy with costs
def mech_design_compare_costs(reset_costs, user_endowment, cost_arrays, prob_arrays, reset_probability_array):
    results = []
    best_index = -1
    max_payoffs = -100000
    
    for i in range(len(cost_arrays)):
        (a, b, x) = one_round(reset_costs, user_endowment, cost_arrays[i], prob_arrays, reset_probability_array)
        results.append([(a, b), a + b, x])
        if (max_payoffs < (a+b)):
            max_payoffs = a + b
            best_index = i
    return results, best_index



if __name__ == '__main__':
    user_endowment = 5

    # Admin costs
    admin_email = -3                                # cost for admin to receive an email for reset                                                                      
    admin_bomb = -5                                 # cost for admin to receive an email bomb for reset
    admin_escalate = -10                            # cost for admin to receive an escalation request for reset
    a_reset = -2                                    # cost for admin for a successful user password reset
    
    # User costs
    pp1_login = -10                                 # weekly cost for user to log in using password that follows PP-1
    pp2_login_pi1 = -12                             # weekly cost for user to log in using password weakened from PP-2
    pp2_login = -14                                 # weekly cost for user to log in using password that follows PP-2

    user_email = -2                                 # cost for user to send an email asking for password reset
    user_bomb = -3                                  # cost for user to send an email bomb asking for password reset
    user_escalate = -5                              # cost for user to ask to escalate for password reset
    u_reset = -1                                    # cost for user for successful password reset

    # Reset probabilities
    prob_initial_reset = gambit.Rational(95,100)    # probability for reset success
    prob_email_reset = gambit.Rational(90,100)      # probability for reset success after sending email to admin
    prob_bomb_reset = gambit.Rational(95,100)       # probability for reset success after sending email bomb to admin

    # Main game probabilities
    # Blacklist policy 
    pi1_nop = gambit.Rational(798,1000)             # probability for NOP when user selects PI-1
    pi1_f = gambit.Rational(127,1000)               # probability for F (forget pw) when user selects PI-1
    pi1_b = gambit.Rational(75,1000)                # probability for B (adversary breaks in) when user selects PI-1

    pi2_nop = gambit.Rational(823,1000)             # probability for NOP when user selects PI-2
    pi2_f = gambit.Rational(127,1000)               # probability for F (forget pw) when user selects PI-2
    pi2_b = gambit.Rational(5,1000)                 # probability for B (adversary breaks in) when user selects PI-2

    # Length policy 
    pi1_nop = gambit.Rational(763,1000)             # probability for NOP when user selects PI-1
    pi1_f = gambit.Rational(127,1000)               # probability for F (forget pw) when user selects PI-1
    pi1_b = gambit.Rational(11,1000)                # probability for B (adversary breaks in) when user selects PI-1

    pi2_nop = gambit.Rational(803,1000)             # probability for NOP when user selects PI-2
    pi2_f = gambit.Rational(127,1000)               # probability for F (forget pw) when user selects PI-2
    pi2_b = gambit.Rational(7,1000)                 # probability for B (adversary breaks in) when user selects PI-2


    # Add each variable to its corresponding array
    reset_costs =   [admin_email, admin_bomb, admin_escalate, a_reset, 
                    user_email, user_bomb, user_escalate, u_reset]
    cost_array = [pp1_login, pp2_login_pi1, pp2_login]
    reset_probability_array = [prob_initial_reset, prob_email_reset, prob_bomb_reset]
    probability_array = [pi1_nop, pi1_f, pi1_b, pi2_nop, pi2_f, pi2_b]

    # Run the simulation with the input parameters, return Nash Equilibrium and payoffs
    (a, b, x) = one_round(reset_costs, user_endowment, cost_array, probability_array, reset_probability_array)

    # Print results of simulation 
    print "The Nash Equilibrium for this give is: {}".format(x[0])
    print "The Admin's final payoff is: {}".format(a)
    print "The User's final payoff is: {}".format(b)
