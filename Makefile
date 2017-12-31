all:
	buildozer android debug deploy run logcat -v | tee log
fix:
	cat log | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\r/,"")}1' | grep "manual"
fixlog:
	cat log | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\r/,"")}1' | tee log
