# compile and send to phone
all:
	adb kill-server
	# all the seds because buildozer ignores all escape characters.
	# sed commands properly print them
	buildozer android debug deploy run | \
	sed 's/\\n/\n/g' | \
	sed 's/\\t/\t/g' | \
	sed 's/\\r/\r/g' | \
	sed "s/'b'//g"
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
