from pysqlcipher3 import dbapi2 as sqlcipher
'''
class to intract with SQLite db file (db.db) located int res folder with password=1
'''
class DBIntract:
	# encrypted db and connect to it with sqlcipher libray
	# check same thread for video and image threads is false because
	# of  the ability to multitreaded functionality of database
	def __init__(self, DBName = "res/db.db", DBPass = "1", checkSameThread = True):
		self.db = sqlcipher.connect(DBName, check_same_thread = checkSameThread)
		self.command = 'pragma key="'+DBPass+'"';
		self.db.execute(self.command)
	
	# Lock at shelves in db and search for appropriate shelf
	# for every shelf we have two socket. one is android and other is
	# one of other sockets (iphone, nokia or type-c).
	def allocateShelf(self, phoneType):
		shelfNum = None
		newType = phoneType
		# Since all shelves have one android socket (with code = 1)
		# if a request for android socket recieved we try to find shelf which
		# distribute other socket types (because that sockets has less ports) availabity evenly.
		if newType == 1:
			# sqlite query extract available shelves that has active sockets
			self.command = """
							drop table if EXISTS tmp;
							drop table if EXISTS tmp1;

							create TEMP table tmp as 
								select SocketID as sid, 
								count(*) as allsockets 
								from ShelfSocket 
								where Active == 1 
								GROUP by SocketID;
								
							create TEMP table tmp1 as 
							select SocketID,count(*) as usedsockets 
							from ShelfSocket, ShelfStatus
							where ShelfSocket.ShelfID = ShelfStatus.ID 
								and ShelfStatus.SocketType <> 0 and ShelfSocket.Active ==1
							GROUP by SocketID;

							"""
			self.db.executescript(self.command)
			# get occupy percentage of other socket types and order them to find most vacant 
			# shelf by socket type
			self.command = """
							select SocketID from
								(select SocketID, 100.0*usedsockets/ allsockets as percent 
								from tmp,tmp1
								where tmp.sid = tmp1.SocketID 
								and SocketID<> 1 
								order by percent ASC)
							limit 1
							"""
			newType = self.db.execute(self.command).fetchone()[0]
		# randomly select one one of candidate shelves
		self.command = 	"""
						select ID 
						from shelfStatus, shelfSocket 
						where shelfStatus.ID == shelfSocket.ShelfID 
						and ShelfSocket.SocketID= ?
						and ShelfStatus.SocketType == 0 
						and ShelfSocket.Active==1
						order by random()
						limit 1
						"""
		shelfNum = self.db.execute(self.command,[newType]).fetchone()[0]
		return shelfNum
		
	def insertUse(self, videoName, startFrame, endFrame, startTime, endTime,
	 picList, shelfNum, socketType, fingerID, inOut):
		self.command = """
						insert into Achievement (StartDT,EndDT,VideoID,
						StartFrame,EndFrame,AchieveType, Fingerprint, Deleted)
						select '{0}', '{1}',
						Video.ID, {2},
						{3}, {4} , '{5}', 0 from Video WHERE Video.Address = '{6}';

						update ShelfStatus set AchievementID = last_insert_rowid(),
						SocketType = '{7}'
						WHERE ID = {8};
						  """.format(startTime, endTime, startFrame, endFrame, inOut, 
						  fingerID, videoName, socketType, shelfNum)
		print("picList ", self.command)
		
		for i in picList:
			print("This Will not Printed")
			self.command.append("""
								insert into Picture (Address, AchievementID,CaptureDT,Deleted)
								select '{0}', last_insert_rowid(), {1} ,0;		
								""".format(i,i[:22]))
		self.db.executescript(self.command)
		return
	
	def insertVideo(self,vidPath):
		print("insert video executes", vidPath[-23:-4])
		self.command = """
						insert into video (Address, StartCaptureDT,EndCaptureDT,Deleted)
						VALUES ('{0}','{1}',0,0)
						""".format(vidPath,vidPath[-23:-4])
		print(self.command)
		self.db.execute(self.command)
	
	def closeVideo(self,vidPath):
		self.command = """
						update video set 
						EndCaptureDT = strftime('%Y-%m-%d %H:%M:%S',datetime('now', 'localtime'))
						where Address = ?
						"""
		self.db.execute(self.command,[vidPath])
		
	#TODO: seperate getOldVid, getOldImg, removeOldVid, removeOldImg to delete and update database
	# and memory in pseudo atomic manner
	def removeOldVidAndImg(self):
		# get address of oldest video by time
		self.command = """
						select Address from Video 
						where Deleted = 0
						order by StartCaptureDT Asc
						limit 1
						"""
						
		vidAddress = self.db.execute(self.command).fetchone()[0]
		# set Deleted field of old video to one (deleted)
		self.command = """
						update Video set Deleted = 1 where 
						Address = ?
						"""
		self.db.execute(self.command,[vidAddress])
		 
		# get list of pictures with age of 30 day or older
		self.command = """
						select Address from Picture where CaptureDT <
						strftime('%Y-%m-%d %H:%M:%S',datetime('now', 'localtime'), '-30 day') 
						and Deleted == 0
						"""
		imgAddress = self.db.execute(self.command).fetchall()
		
		# set Deleted field of old images to one (deleted)
		self.command = """
						update Picture set Deleted = 1 where 
						id=(select id from Picture where CaptureDT <
						strftime('%Y-%m-%d %H:%M:%S',datetime('now', 'localtime'), '-30 day') 
						and Deleted == 0)
						"""
		self.db.execute(self.command)	
		
		# return video and images address to free up them from memory
		files = [vidAddress, imgAddress]		
		
		return files
						
	def adminCheck(self, pwd):
		admin = None

		self.command = 	"""
						select User 
						from adm 
						where ps == ?
						"""
		
		admin = self.db.execute(self.command,[pwd]).fetchone()[0]
		return admin
		
		
