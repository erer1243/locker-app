all:
	adb kill-server
	buildozer android debug deploy run
log: all
	adb kill-server
	adb logcat | grep locker-controller
