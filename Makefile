all:
	adb -P 5038 kill-server
	adb kill-server
	buildozer android debug deploy run
log:
	adb -P 5038 kill-server
	buildozer android debug deploy run
	adb kill-server
	../logcat | grep locker-controller
