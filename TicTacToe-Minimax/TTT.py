import copy

DEBUG = False

class TicTacToe:
	def __init__ ( self, size, player, cutoffLimit ):

		# 0 stands for an empty cell
		self.state = [[ 0 for x in range( size ) ] for y in range( size ) ]
		self.size = size 
		self.player = player
		self.cutoff_limit = cutoffLimit
		self.check = False

	def player( self ):
		""" There are two possible players, "X" and "O". """
		if self.player == 'X':
			self.player = 'O'
		else:
			self.player = 'X'	

	def actions( self, state ):

		# Store indexes of empty cell
		actionlst = []
		sz = self.size
		for i in range( sz ):
			for j in range( sz ):
				if ( state[ i ][ j ]) == 0:
					actionlst.append( ( i, j ) )
		return actionlst

	def results( self, state, index ):
		if self.player == 'X':
			state[ index[ 0 ] ][ index[ 1 ] ] = 'x'
		else:
			state[ index[ 0 ] ][ index[ 1 ] ] = 'o'
		return state	

	def cutoff_Test( self, state, depth ):
		if ( depth >= self.cutoff_limit ) or ( self.checkZero( state ) ):
			return True
		else:
			return False
		
	def evaluation( self, state, player, depth ):
		sz = 3	
		cost = 0
		x_count = 0
		o_count = 0
		# Check each rows
		for i in range( sz ):
			if 'o' in state[i]:
				continue 
			for j in range( sz ):
				if state[ i ][ j ] == 'x':
					x_count += 1	
			if x_count == 3:
				cost += 1000
			elif x_count == 2:
				cost += 100
			elif x_count == 1:
				cost += 10
			elif x_count == 0:
				cost += 1		
			x_count = 0	
		if DEBUG: print(cost) 
		
		# Check each columns				
		for i in range( sz ):
			for j in range( sz ):
				if state[ j ][ i ] == 'x':
					x_count += 1
					if DEBUG: print(x_count) 
				elif state[ j ][ i ] == 'o':
					x_count = -1
					break	
			if x_count == 3:
				cost += 1000
			elif x_count == 2:
				cost += 100
			elif x_count == 1:
				cost += 10
			elif x_count == 0:
				cost += 1	
			x_count = 0			 
		if DEBUG: print(cost) 

		# Check for positive diagonal
		for i in range( sz ):
			if state[ i ][ i ] == 'o':
				x_count = -1	# So it won't match any cost below
				break
			elif state[ i ][ i ] == 'x':
					x_count += 1
		if x_count == 3:
			cost += 1000
		elif x_count == 2:
			cost += 100
		elif x_count == 1:
			cost += 10
		elif x_count == 0:
			cost += 1	
		x_count = 0				
		if DEBUG: print(cost) 

		# Check for negative diagonal
		j = sz -1   # column 
		i = 0   # row
		while j != -1:
			if state[ i ][ j ] == 'o':
				x_count = -1	# So it won't match any cost below
				break	
			elif state[ i ][ j ] == 'x':
				x_count += 1	
			i += 1
			j -= 1
		if x_count == 3:
			cost += 1000
		elif x_count == 2:
			cost += 100
		elif x_count == 1:
			cost += 10
		elif x_count == 0:
			cost += 1	
		x_count = 0				
		if DEBUG: print(cost) 

		# Check each rows
		for i in range( sz ):
			if 'x' in state[i]:
				continue 
			for j in range( sz ):
				if state[ i ][ j ] == 'o':
					o_count += 1
			if o_count == 3:
				cost += -1000
			elif o_count == 2:
				cost += -100
			elif o_count == 1:
				cost += -10
			elif o_count == 0:
				cost += -1		
			o_count = 0	
		if DEBUG: print(cost) 
		
		# Check each columns
		tf = False				
		for i in range( sz ):
			for j in range( sz ):
				if state[ j ][ i ] == 'o':
					o_count += 1
				elif state[ j ][ i ] == 'x':
					o_count = 0
					tf = True
					break	
			if not tf: 		
				if o_count == 3:
					cost += -1000
				elif o_count == 2:
					cost += -100
				elif o_count == 1:
					cost += -10
				elif o_count == 0:
					cost += -1	
				o_count = 0			 
		if DEBUG: print(cost) 

		# Check for positive diagonal
		for i in range( sz ):
			if state[ i ][ i ] == 'x':
				o_count = -1	# So it won't match any cost below
				break
			elif state[ i ][ i ] == 'o':
					o_count += 1
		if o_count == 3:
			cost += -1000
		elif o_count == 2:
			cost += -100
		elif o_count == 1:
			cost += -10
		elif o_count == 0:
			cost += -1	
		o_count = 0				
		if DEBUG: print(cost) 

		# Check for negative diagonal
		j = sz -1   # column 
		i = 0   # row
		while j != -1:
			if state[ i ][ j ] == 'x':
				o_count = -1	# So it won't match any cost below
				break	
			elif state[ i ][ j ] == 'o':
				o_count += 1	
			i += 1
			j -= 1
		if o_count == 3:
			cost += -1000
		elif o_count == 2:
			cost += -100
		elif o_count == 1:
			cost += -10
		elif o_count == 0:
			cost += -1	
		o_count = 0				
		if DEBUG: print(cost) 
		if DEBUG: print("evaluation selfcheck:", self.check)
		return cost * ( 4 - depth ) 				


	def checkZero( self, state ):
		""" A helper function to check whether there are empty cells 
		in the game."""
		sz = self.size
		for i in range( sz ):
			for j in range( sz ):
				if ( state[ i ][ j ]) == 0:
					return False
		return True  	

def checkend( state ):
	
	# Check row
	for i in state:
		if not ( 0 in i or 'o' in i ):
			return True
		elif not ( 0 in i or 'x'in i ):			
			return True

	# Check column
	x_count = 0
	o_count = 0
	for i in range( 3 ):
		for j in range( 3 ):
			if state[ j ][ i ] == 'x':
				x_count += 1
			elif state[ j ][ i ] == 'o':
				o_count += 1
		if x_count == 3 or o_count == 3:				
			return True
		x_count = 0
		o_count = 0	

	# Check positive diagoal 
	x_count = 0
	o_count = 0
	for i in range( 3 ):
		if state[ i ][ i ] == 'x':
			x_count += 1	
		elif state[ i ][ i ] == 'o':
			o_count += 1
	if x_count == 3 or o_count == 3:				
		return True

	# Check negative diagonal
	j = 2   # column 
	i = 0   # row
	x_count = 0
	o_count = 0
	while j != -1:
		if state[ i ][ j ] == 'x':
			x_count += 1	
		elif state[ i ][ j ] == 'o':
			o_count += 1	
		i += 1
		j -= 1
	if x_count == 3 or o_count == 3:				
		return True	
	return False

def Alpha_Beta_Search( game ):
	pInf = float( "inf" )
	nInf = -float( "inf" )
	newstate = copy.deepcopy( game.state )
	result = Max_value( newstate, nInf, pInf, game, 0 )
	if type(result) == int:
		if DEBUG: print(result) 
		if DEBUG: print(game.state) 
		return game
	else:
		if DEBUG: print(result[ 1 ])
		game.results( game.state, result[ 1 ] )
		if DEBUG: print(game.state)
		return game


def Max_value( state, alpha, beta, game, depth ):
	game.player = 'X'
	if game.cutoff_Test( state, depth ) or checkend( state ):
		game.player = 'O'
		if game.check:
			if DEBUG: print("gamecheck shi duide") 
		return game.evaluation( state, game.player, depth )
	if DEBUG: print("State is: ",state,"\n") 
	if DEBUG: print("Depth is: ", depth, "\n") 
	v = -float( "inf" )
	actions = game.actions( state )
	best_action = actions[ 0 ]
	if DEBUG: print(actions)
	count = 0
	for a in actions:
		if DEBUG: print("count",count) 
		if DEBUG: print("action", a) 
		count +=1
		newstate = copy.deepcopy( state )
		newstate = game.results( newstate, a )
		if DEBUG: print("MaxNewstate is: ", newstate,"\n") 

		nextn = Min_value( newstate, alpha, beta, game, depth + 1 )
		if type( nextn ) != int:
			if v < nextn[ 0 ]:
				v = nextn[ 0 ]
				best_action = a
			if v >= beta:
				game.player = 'X'
				if DEBUG: print("best_action is: ", best_action,"\n") 
				if DEBUG: print("\n\n\n\n") 
				return ( v, best_action )
		else:
			if v < nextn:
				v = nextn
				best_action = a
			if v >= beta:
				game.player = 'O'
				if DEBUG: print("best_action is: ", best_action,"\n") 
				if DEBUG: print("\n\n\n\n") 
				return ( v, best_action )		
		alpha = max( alpha, v )

	if DEBUG: print("best_action is: ", best_action,"\n") 
	if DEBUG: print("\n\n\n\n") 
	game.player = 'O'	
	return ( v, best_action )		


def Min_value( state, alpha, beta, game, depth ):
	game.player = 'O'
	if DEBUG: print("Min") 
	if game.cutoff_Test( state, depth ) or checkend( state ) :
		if DEBUG: print("Min jin") 
		game.player = 'X'
		if DEBUG: print("zuihou", state) 
		if game.check:
			if DEBUG: print("gamecheck shi duide") 
		return game.evaluation( state, game.player, depth )
	if DEBUG: print("after jin") 
	if DEBUG: print("State is: ",state,"\n") 
	if DEBUG: print("Depth is: ", depth, "\n") 
	v = float( "inf" ) 
	actions = game.actions( state )
	best_action = actions[ 0 ] 
	for a in game.actions( state ):
		newstate = copy.deepcopy( state )
		newstate = game.results( newstate, a )

		if DEBUG: print("MinNew state is: ", newstate,"\n") 
		nextn = Max_value( newstate, alpha, beta, game, depth + 1 )
		if type( nextn ) != int: 
			if v > nextn[ 0 ]: 
				v = nextn[ 0 ]
				best_action = a
			if v <= alpha:
				game.player = 'X'
				if DEBUG: print("best_action is: ", best_action,"\n") 
				if DEBUG: print("\n\n\n\n") 
				return ( v, best_action ) 
		else:
			if v > nextn: 
				v = nextn
				best_action = a
			if v <= alpha:
				game.player = 'X'
				if DEBUG: print("best_action is: ", best_action,"\n") 
				if DEBUG: print("\n\n\n\n") 
				return ( v, best_action ) 		
		beta = min( beta, v )
	if DEBUG: print("best_action is: ", best_action,"\n") 
	if DEBUG: print("\n\n\n\n") 
	game.player = 'X'		
	return ( v, best_action )