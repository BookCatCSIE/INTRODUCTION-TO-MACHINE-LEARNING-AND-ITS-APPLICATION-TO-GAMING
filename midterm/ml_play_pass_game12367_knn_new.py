"""The template of the main script of the machine learning process
"""

from .. import communication as comm
from ..communication import SceneInfo, GameInstruction
import pickle, time
import numpy as np
#import os.path
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
	#c=100
	#d=100
	# 2. Inform the game process that ml process is ready before start the loop.
	frame_ind=[]
	ballpos=[]
	platform=[]
	instruct=[]
	des_test=[]
	#LL=[]
	#LL2=[]
	filename="neigh_knn_game12367_0523.sav"
	load_model=pickle.load(open(filename, 'rb'))
	#filename="neigh_knn_game12367_0523.sav" 
	#filepath = os.path.join(os.path.dirname(__file__), filename)
	#load_model=pickle.load(open(filepath, 'rb'))
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
		# inp_temp=np.array([scene_info.ball[0], scene_info.ball[1], scene_info.platform[0]])
		# input=inp_temp[np.newaxis, :]
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
		m=((d-b)/(c-a))
		L=(400-d+c*m)/m
		#LL.append(L)
		#px=0
		
		### inp_temp=np.array([scene_info.ball[0], scene_info.ball[1], scene_info.platform[0], K, ((d-b)/(c-a)), (c-a), (d-b), K2, a, b])
		#inp_temp=np.array([L, scene_info.platform[0]])
		#input=inp_temp[np.newaxis, :]
		
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
		
		if load_model.predict(input)==1:
			comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
			instruct.append(1)
		elif load_model.predict(input)==-1:
			comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
			instruct.append(-1)
		else:
			comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
			instruct.append(0)
		
		#LL2.append(L)
		
		# if L>=0 and L<=200:
			# L = L
		# elif L<0 and L>-200:
			# L = -L
		# elif L>200 and L<400:
			# L = 400-L
		
		# if L>=0 and L<20:
			# px=0
		# elif L>=20 and L<40:
			# px=10
		# elif L>=40 and L<60:
			# px=30
		# elif L>=60 and L<80:
			# px=50
		# elif L>=80 and L<100:
			# px=70
		# elif L>=100 and L<120:
			# px=90
		# elif L>=120 and L<140:
			# px=110
		# elif L>=140 and L<160:
			# px=130
		# elif L>=160 and L<180:
			# px=150
		# elif L>=180 and L<200:
			# px=160
		
		
		# if scene_info.platform[0]<px:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_RIGHT)
			# instruct.append(1)
		# elif scene_info.platform[0]>px:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_LEFT)
			# instruct.append(-1)
		# else:
			# comm.send_instruction(scene_info.frame, GameInstruction.CMD_NONE)
			# instruct.append(0)

