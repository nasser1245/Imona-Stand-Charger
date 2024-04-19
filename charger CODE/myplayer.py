import vlc
import sys
import tkinter as Tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time

class Player(Tk.Frame):
	_geometry = ''
	_stopped  = None

	def __init__(self, parent, title=None, video=''):
		Tk.Frame.__init__(self, parent)
		self.parent = parent  # == root
		self.parent.title(title or "tkVLCplayer")
		self.video = expanduser(video)

		self.videopanel = ttk.Frame(self.parent)

		self.canvas = Tk.Canvas(self.videopanel)
		self.canvas.pack(fill=Tk.BOTH, expand=1)
		self.videopanel.pack(fill=Tk.BOTH, expand=1)

    	        # panel to hold buttons
		buttons = ttk.Frame(self.parent)
		self.playButton = ttk.Button(buttons, text="Play", command=self.OnPlay)
		stop            = ttk.Button(buttons, text="Stop", command=self.OnStop)
		#self.muteButton = ttk.Button(buttons, text="Mute", command=self.OnMute)
		self.playButton.pack(side=Tk.LEFT)
		stop.pack(side=Tk.LEFT)
        # self.muteButton.pack(side=Tk.LEFT)

        # self.volMuted = False
        # self.volVar = Tk.IntVar()
        # self.volSlider = Tk.Scale(buttons, variable=self.volVar, command=self.OnVolume,
        #                           from_=0, to=100, orient=Tk.HORIZONTAL, length=200,
        #                           showvalue=0, label='Volume')
        # self.volSlider.pack(side=Tk.LEFT)
		buttons.pack(side=Tk.BOTTOM)

        # panel to hold player time slider
		timers = ttk.Frame(self.parent)
		self.timeVar = Tk.DoubleVar()
		self.timeSliderLast = 0
		self.timeSlider = Tk.Scale(timers, variable=self.timeVar, command=self.OnTime,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500,
                                   showvalue=0)  # label='Time',
		self.timeSlider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
		self.timeSliderUpdate = time.time()
		timers.pack(side=Tk.BOTTOM, fill=Tk.X)

                # VLC player
		args = []
		#if _isLinux:
		#	args.append('--no-xlib')
		self.Instance = vlc.Instance(args)
		self.player = self.Instance.media_player_new()

		self.parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
		self.parent.update()

		self.OnTick()  # set the timer up

	def OnClose(self, *unused):

        # print("_quit: bye")
		self.parent.quit()  # stops mainloop
		self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate
		sys.exit(0)

	def OnConfigure(self, *unused):

        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
		self._geometry = ''  # force .OnResize in .OnTick, recursive?


	def _Pause_Play(self, playing):
        # re-label menu item and button, adjust callbacks
		p = 'Pause' if playing else 'Play'
		c = self.OnPlay if playing is None else self.OnPause
		self.fileMenu.entryconfig(self.playIndex, label=p, command=c)
        # self.fileMenu.bind_shortcut('p', c)  # XXX handled
		self.playButton.config(text=p, command=c)
		self._stopped = False

	def _Pause_Play(self, playing):
        # re-label menu item and button, adjust callbacks
		p = 'Pause' if playing else 'Play'
		c = self.OnPlay if playing is None else self.OnPause
		#self.fileMenu.entryconfig(self.playIndex, label=p, command=c)
        # self.fileMenu.bind_shortcut('p', c)  # XXX handled
		self.playButton.config(text=p, command=c)
		self._stopped = False

	def _Play(self, video):
        # helper for OnOpen and OnPlay
		if isfile(video):  # Creation
			m = self.Instance.media_new(str(video))  # Path, unicode
			self.player.set_media(m)
			self.parent.title("tkVLCplayer - %s" % (basename(video),))

            # set the window id where to render VLC's video output
			h = self.videopanel.winfo_id()  # .winfo_visualid()?
			#if _isWindows:
			self.player.set_hwnd(h)
			#elif _isMacOS:
                # XXX 1) using the videopanel.winfo_id() handle
                # causes the video to play in the entire panel on
                # macOS, covering the buttons, sliders, etc.
                # XXX 2) .winfo_id() to return NSView on macOS?
			#	v = _GetNSView(h)
			#	if v:
			#		self.player.set_nsobject(v)
			#	else:
			#		self.player.set_xwindow(h)  # plays audio, no video
			#else:
			#	self.player.set_xwindow(h)  # fails on Windows
            # FIXME: this should be made cross-platform
			self.OnPlay()

	def OnPause(self, *unused):

		if self.player.get_media():
			self._Pause_Play(not self.player.is_playing())
			self.player.pause()  # toggles

	def OnPlay(self, *unused):

        # if there's no video to play or playing,
        # open a Tk.FileDialog to select a file
		if not self.player.get_media():
			if self.video:
				self._Play(expanduser(self.video))
				self.video = ''
			else:
				self.OnOpen()
        # Try to play, if this fails display an error message
		elif self.player.play():  # == -1
			self.showError("Unable to play the video.")
		else:
			self._Pause_Play(True)
            # set volume slider to audio level
			# vol = self.player.audio_get_volume()
			# if vol > 0:
   #              self.volVar.set(vol)
   #              self.volSlider.set(vol)

	def OnStop(self, *unused):

		if self.player:
			self.player.stop()
			self._Pause_Play(None)
            # reset the time slider
			self.timeSlider.set(0)
			self._stopped = True
        # XXX on macOS libVLC prints these error messages:
        # [h264 @ 0x7f84fb061200] get_buffer() failed
        # [h264 @ 0x7f84fb061200] thread_get_buffer() failed
        # [h264 @ 0x7f84fb061200] decode_slice_header error
        # [h264 @ 0x7f84fb061200] no frame!

	def OnTick(self):

		if self.player:
            # since the self.player.get_length may change while
            # playing, re-set the timeSlider to the correct range
			t = self.player.get_length() * 1e-3  # to seconds
			if t > 0:
				self.timeSlider.config(to=t)

				t = self.player.get_time() * 1e-3  # to seconds
                # don't change slider while user is messing with it
				if t > 0 and time.time() > (self.timeSliderUpdate + 2):
					self.timeSlider.set(t)
					self.timeSliderLast = int(self.timeVar.get())
        # start the 1 second timer again
		self.parent.after(1000, self.OnTick)
        # adjust window to video aspect ratio, done periodically
        # on purpose since the player.video_get_size() only
        # returns non-zero sizes after playing for a while
		#if not self._geometry:
		#	self.OnResize()

	def OnTime(self, *unused):
		if self.player:
			t = self.timeVar.get()
			if self.timeSliderLast != int(t):
                # this is a hack. The timer updates the time slider.
                # This change causes this rtn (the 'slider has changed' rtn)
                # to be invoked.  I can't tell the difference between when
                # the user has manually moved the slider and when the timer
                # changed the slider.  But when the user moves the slider
                # tkinter only notifies this rtn about once per second and
                # when the slider has quit moving.
                # Also, the tkinter notification value has no fractional
                # seconds.  The timer update rtn saves off the last update
                # value (rounded to integer seconds) in timeSliderLast if
                # the notification time (sval) is the same as the last saved
                # time timeSliderLast then we know that this notification is
                # due to the timer changing the slider.  Otherwise the
                # notification is due to the user changing the slider.  If
                # the user is changing the slider then I have the timer
                # routine wait for at least 2 seconds before it starts
                # updating the slider again (so the timer doesn't start
                # fighting with the user).
				self.player.set_time(int(t * 1e3))  # milliseconds
				self.timeSliderUpdate = time.time()


if __name__ == "__main__":

	_video = 'e:\\film\\Game.of.Thrones.S01E01.720p.Film.Mojoo.ir.mkv'
	root = Tk.Tk()
	player = Player(root, video=_video)
	root.protocol("WM_DELETE_WINDOW", player.OnClose)  # XXX unnecessary (on macOS)
	root.mainloop()