SOURCES=workload.py


.PHONY: all
all: out

go-1.17.4-r0.apk:
	wget https://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/go-1.17.4-r0.apk

out: ${SOURCES} go-1.17.4-r0.apk
	mkdir -p out
	cp ${SOURCES} out
	tar -C out -xzf go-1.17.4-r0.apk usr/lib 2> /dev/null
