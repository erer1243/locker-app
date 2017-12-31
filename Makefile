all:
	buildozer android debug deploy run
log:
	buildozer android debug deploy run
	adb kill-server
	../logcat | grep locker-controller
