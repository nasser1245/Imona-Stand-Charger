import vlc
from time import sleep
Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new_path('f:\\2019.avi')
player.set_media(Media)
player.play()
sleep(5)
while player.is_playing():
     sleep(1)