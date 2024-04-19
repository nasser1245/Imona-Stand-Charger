
from pyfingerprint.pyfingerprint import PyFingerprint

class fingerprint(object):
	def __init__(self, port = '/dev/ttyS1', baudRate = 57600, address = 0xFFFFFFFF, password = 0x00000000):

		try:
			f = PyFingerprint('/dev/ttyS1', 57600, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			exit(1)
			
	def enroll(self, shelfNum):
		print("1")
		
