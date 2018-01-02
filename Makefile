all: custom_java
	adb -P 5038 kill-server
	adb kill-server
	buildozer android debug deploy run
log: all
	adb kill-server
	../logcat | grep locker-controller
custom_java: clean_java
	javac ./java/*.java
	jar cvf ./java/BluetoothGattCallback.jar ./java/*
clean_java:
	rm -f java/*.class java/*.jar java/build
