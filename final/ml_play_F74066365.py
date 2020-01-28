"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pingpong.communication as comm
from pingpong.communication import (
	SceneInfo, GameInstruction, GameStatus, PlatformAction
)
import pickle, time
import numpy as np
import os.path
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
	# filename1="pingpong_model_p1.sav"
	# load_model_p1=pickle.load(open(filename1, 'rb'))
	# filename2="pingpong_model_p2.sav"
	# load_model_p2=pickle.load(open(filename2, 'rb'))
	# comm.ml_ready()

	# 3. Start an endless loop
	if side=='1P':
		# filename="F74066365_p1_svm_ver3.sav"
		# load_model_p1=pickle.load(open(filename, 'rb'))
		filename="F74066365_p1_svm_ver3.sav" 
		filepath = os.path.join(os.path.dirname(__file__), filename)
		load_model_p1=pickle.load(open(filepath, 'rb'))
		
		comm.ml_ready()
		
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
		
		# 3.4 Send the instruction for this frame to the game process
			inp_temp=np.array([c,d,(c-a),(d-b)])
			input=inp_temp[np.newaxis, :]
			L = load_model_p1.predict(input)
				
			if scene_info.platform_1P[0]+20>L+3:  #+4  +2.5
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
			elif scene_info.platform_1P[0]+20<L+2:  #+1  +2.5
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
			else:
				comm.send_instruction(scene_info.frame, PlatformAction.NONE)
			
	else:
		# filename="F74066365_p2_svm_ver3.sav"
		# load_model_p2=pickle.load(open(filename, 'rb'))
		filename="F74066365_p2_svm_ver3.sav" 
		filepath = os.path.join(os.path.dirname(__file__), filename)
		load_model_p2=pickle.load(open(filepath, 'rb'))
		
		comm.ml_ready()
		
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
		
		# 3.4 Send the instruction for this frame to the game process
			inp_temp=np.array([c,d,(c-a),(d-b)])
			input=inp_temp[np.newaxis, :]
			L = load_model_p2.predict(input)
			
			if scene_info.platform_2P[0]+20>L+3:  #+4
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
			elif scene_info.platform_2P[0]+20<L+2:  #+1
				comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
			else:
				comm.send_instruction(scene_info.frame, PlatformAction.NONE)
	