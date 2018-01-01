all:
	pkill adb
	-adb -P 5038 kill-server
	-adb kill-server
	buildozer android debug deploy run
log: all
	adb kill-server
	../logcat | grep locker-controller
