"""The template of the main script of the machine learning process
"""

from .. import communication as comm
from ..communication import SceneInfo, GameInstruction
import pickle, time
import numpy as np
import os.path
def ml_loop():
	"""The main loop of the machine learning process

	This loop is run in a seperate process, and communicates with the game process.

	Note that the game process won't wait for the ml process to generate the
	GameInstrcution. It is possible that the frame of the GameInstruction
	is behind of the current frame in the game process. Try to decrease the fps
	to avoid this situation.
	"""

	# === Here is the execution order of the loop === #
	# 1. Put the initialization code here.
	a=0
	b=0
	c=93
	d=93
	# 2. Inform the game process that ml process is ready before start the loop.
	frame_ind=[]
	ballpos=[]
	platform=[]
	instruct=[]
	des_test=[]
	#filename="neigh_knn_game12367_0523.sav"
	#load_model=pickle.load(open(filename, 'rb'))
	filename="neigh_knn_game12367_0523.sav" 
	filepath = os.path.join(os.path.dirname(__file__), filename)
	load_model=pickle.load(open(filepath, 'rb'))
	comm.ml_ready()

	# 3. Start an endless loop.
	while True:
		# 3.1. Receive the scene information sent from the game process.
		scene_info = comm.get_scene_info()
		frame_ind.append(scene_info.frame)
		ballpos.append(scene_info.ball)
		platform.append(scene_info.platform)
		#all_infor=[frame_ind, ballpos, platform, instruct]
		#all_infor=[frame_ind, ballpos, platform, instruct, LL, LL2]
		# 3.2. If the game is over or passed, the game process will reset
		#      the scene immediately and send the scene information again.
		#      Therefore, receive the reset scene information.
		#      You can do proper actions, when the game is over or passed.
		if scene_info.status == SceneInfo.STATUS_GAME_OVER or \
			scene_info.status == SceneInfo.STATUS_GAME_PASS:
			#save game data
			#fname='game_infor'+time.strftime("%m_%d_%H_%M_%S", time.localtime())+'.pickle'
			#file=open(fname, 'wb')
			#pickle.dump(all_infor, file)
			#file.close()
			# fname2='des_infor'+time.strftime("%m_%d_%H_%M_%S", time.localtime())+'.pickle'
			# file2=open(fname2, 'wb')
			# pickle.dump(des_test, file2)
			# file2.close()
			scene_info = comm.get_scene_info()

		# 3.3. Put the code here to handle the scene information
		a=c
		b=d
		c=scene_info.ball[0]
		d=scene_info.ball[1]
		if c-a==0:
			m=((d-b)/1)
		else:
			m=((d-b)/(c-a))
		# m=((d-b)/(c-a))    --> exception: divided by zero
		L=(400-d+c*m)/m
		t1=d-b
		t2=c-a
		
		if L>=0 and L<=200:
			L = L
		elif L<0:
			#L = (-L)%200
			L = -L
			num = L//200
			rr = L%200
			if num%2==1:
				L = 200-rr
			else:
				L = rr
		elif L>200:
			#L = 200-(L-200)%200
			L = L-200
			num = L//200
			rr = L%200
			if num%2==1:
				L = rr
			else:
				L = 200-rr
		
		# 3.4. Send the instruction for this frame to the game process      
		
		
		inp_temp=np.array([L, scene_info.platform[0]])
		input=inp_temp[np.newaxis, :]
		
		if t1>0:
			if load_model.predict(input)==1:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
				instruct.append(1)
			elif load_model.predict(input)==-1:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
				instruct.append(-1)
			else:
				comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
				instruct.append(0)
		else:
			if t2<0:
				# comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
				# instruct.append(-1)
				if c>100:
					comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
					instruct.append(-1)
				else:
					comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
					instruct.append(1)
				# if scene_info.platform[0]>30:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
					# instruct.append(-1)
				# elif scene_info.platform[0]<30:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
					# instruct.append(1)
				# else:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
					# instruct.append(0)
			else:
				if c>100:
					comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
					instruct.append(-1)
				else:
					comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
					instruct.append(1)
				
				# if scene_info.platform[0]>150:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
					# instruct.append(-1)
				# elif scene_info.platform[0]<150:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
					# instruct.append(1)
				# else:
					# comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
					# instruct.append(0)
			
			
			
			
			
		# if load_model.predict(input)==1:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
			# instruct.append(1)
		# elif load_model.predict(input)==-1:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
			# instruct.append(-1)
		# else:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
			# instruct.append(0)
		

