"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pingpong.communication as comm
from pingpong.communication import (
	SceneInfo, GameInstruction, GameStatus, PlatformAction
)

def ml_loop(side: str):
	"""
	The main loop for the machine learning process

	The `side` parameter can be used for switch the code for either of both sides,
	so you can write the code for both sides in the same script. Such as:
	```python
	if side == "1P":
		ml_loop_for_1P()
	else:
		ml_loop_for_2P()
	```

	@param side The side which this script is executed for. Either "1P" or "2P".
	"""

	# === Here is the execution order of the loop === #
	# 1. Put the initialization code here
	c=100
	d=250
	LL2=0  #global variable
	# 2. Inform the game process that ml process is ready
	comm.ml_ready()

	# 3. Start an endless loop
	if side=='1P':
		while True:
		# 3.1. Receive the scene information sent from the game process
			scene_info = comm.get_scene_info()

		# 3.2. If either of two sides wins the game, do the updating or
		#      reseting stuff and inform the game process when the ml process
		#      is ready.
			if scene_info.status == GameStatus.GAME_1P_WIN or \
				scene_info.status == GameStatus.GAME_2P_WIN:
				# Do something updating or reseting stuff

				# 3.2.1 Inform the game process that
				#       the ml process is ready for the next round
				comm.ml_ready()
				continue

		# 3.3 Put the code here to handle the scene information
			a=c
			b=d
			c=scene_info.ball[0]
			d=scene_info.ball[1]
			if c-a==0:
				m=((d-b)/1)
			else:
				m=((d-b)/(c-a))
		
		# 3.4 Send the instruction for this frame to the game process
			if d-b<0:
				L=(80-d+c*m)/m
				
				if L>=0 and L<=200:
					L = L
				elif L<0:
					L = -L
					num = L//200
					rr = L%200
					if num%2==1:
						L = 200-rr
					else:
						L = rr
				elif L>200:
					L = L-200
					num = L//200
					rr = L%200
					if num%2==1:
						L = rr
					else:
						L = 200-rr
				
				if scene_info.platform_1P[0]+20>L+3:  #+4  +2.5
					comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
				elif scene_info.platform_1P[0]+20<L+2:  #+1  +2.5
					comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
				else:
					comm.send_instruction(scene_info.frame, PlatformAction.NONE)
			else:
				if d<215:
					L=(215-d+c*m)/m
					
					if L>=0 and L<=200:
						L = L
					elif L<0:
						L = -L
						num = L//200
						rr = L%200
						if num%2==1:
							L = 200-rr
						else:
							L = rr
					elif L>200:
						L = L-200
						num = L//200
						rr = L%200
						if num%2==1:
							L = rr
						else:
							L = 200-rr
					
					m2=(-1/m)
					L2=(80-215+L*m2)/m2
					
					if L2>=0 and L2<=200:
						L2 = L2
					elif L2<0:
						L2 = -L2
						num = L2//200
						rr = L2%200
						if num%2==1:
							L2 = 200-rr
						else:
							L2 = rr
					elif L2>200:
						L2 = L2-200
						num = L2//200
						rr = L2%200
						if num%2==1:
							L2 = rr
						else:
							L2 = 200-rr
					
					LL2=L2
					
					if scene_info.platform_1P[0]+20>L2+3:  #+4  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
					elif scene_info.platform_1P[0]+20<L2+2:  #+1  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
					else:
						comm.send_instruction(scene_info.frame, PlatformAction.NONE)
				else:
					if scene_info.platform_1P[0]+20>LL2+3:  #+4  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
					elif scene_info.platform_1P[0]+20<LL2+2:  #+1  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
					else:
						comm.send_instruction(scene_info.frame, PlatformAction.NONE)
			
	else:
		while True:
		# 3.1. Receive the scene information sent from the game process
			scene_info = comm.get_scene_info()

		# 3.2. If either of two sides wins the game, do the updating or
		#      reseting stuff and inform the game process when the ml process
		#      is ready.
			if scene_info.status == GameStatus.GAME_1P_WIN or \
				scene_info.status == GameStatus.GAME_2P_WIN:
				# Do something updating or reseting stuff

				# 3.2.1 Inform the game process that
				#       the ml process is ready for the next round
				comm.ml_ready()
				continue

		# 3.3 Put the code here to handle the scene information
			a=c
			b=d
			c=scene_info.ball[0]
			d=scene_info.ball[1]
			if c-a==0:
				m=((d-b)/1)
			else:
				m=((d-b)/(c-a))
		
		# 3.4 Send the instruction for this frame to the game process
			if d-b>0:
				L=(415-d+c*m)/m
				
				if L>=0 and L<=200:
					L = L
				elif L<0:
					L = -L
					num = L//200
					rr = L%200
					if num%2==1:
						L = 200-rr
					else:
						L = rr
				elif L>200:
					L = L-200
					num = L//200
					rr = L%200
					if num%2==1:
						L = rr
					else:
						L = 200-rr
				
				if scene_info.platform_2P[0]+20>L+3:  #+4
					comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
				elif scene_info.platform_2P[0]+20<L+2:  #+1
					comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
				else:
					comm.send_instruction(scene_info.frame, PlatformAction.NONE)
			else:
				if d>280:
					L=(280-d+c*m)/m
					
					if L>=0 and L<=200:
						L = L
					elif L<0:
						L = -L
						num = L//200
						rr = L%200
						if num%2==1:
							L = 200-rr
						else:
							L = rr
					elif L>200:
						L = L-200
						num = L//200
						rr = L%200
						if num%2==1:
							L = rr
						else:
							L = 200-rr
					
					m2=(-1/m)
					#L2=(416-280+L*m2)/m2
					L2=(415-280+L*m2)/m2
					
					if L2>=0 and L2<=200:
						L2 = L2
					elif L2<0:
						L2 = -L2
						num = L2//200
						rr = L2%200
						if num%2==1:
							L2 = 200-rr
						else:
							L2 = rr
					elif L2>200:
						L2 = L2-200
						num = L2//200
						rr = L2%200
						if num%2==1:
							L2 = rr
						else:
							L2 = 200-rr
					
					LL2=L2
					
					if scene_info.platform_2P[0]+20>L2+3:  #+4  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
					elif scene_info.platform_2P[0]+20<L2+2:  #+1  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
					else:
						comm.send_instruction(scene_info.frame, PlatformAction.NONE)
				else:
					if scene_info.platform_2P[0]+20>LL2+3:  #+4  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
					elif scene_info.platform_2P[0]+20<LL2+2:  #+1  +2.5
						comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
					else:
						comm.send_instruction(scene_info.frame, PlatformAction.NONE)
				