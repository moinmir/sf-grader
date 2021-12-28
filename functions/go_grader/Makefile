SOURCES=workload.py


.PHONY: all
all: out

go-1.17.4-r0.apk:
	wget https://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/go-1.17.4-r0.apk

out/usr/lib/go/lib/tool/linux_amd64/test2json: go-1.17.4-r0.apk
	mkdir -p out
	tar -C out -xzf go-1.17.4-r0.apk usr/lib/go/pkg/tool/linux_amd64/test2json 2> /dev/null

out: ${SOURCES} out/usr/lib/go/lib/tool/linux_amd64/test2json
	mkdir -p out
	cp ${SOURCES} out
