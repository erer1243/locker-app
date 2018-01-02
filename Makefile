# compile and send to phone
all:
	adb kill-server
	buildozer android debug deploy run
# log only from app
log: all
	adb kill-server
	adb logcat | grep locker-controller
# to give opportunity to begin logging manually within make script
manual_log: all
	adb kill-server
	@echo "Enter to begin logging"
	@read x
	adb logcat | grep locker-controller
