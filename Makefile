
output/%.img: functions/%/*
	@truncate -s 500M $@
	@mkfs.ext4 -F $@
	@ \
		if [ -f functions/$*/Makefile ]; then \
			make -C functions/$*; \
			cptofs -t ext4 -i $@ functions/$*/out/* /; \
		else \
			cptofs -t ext4 -i $@ functions/$*/* /; \
		fi
	@e2fsck -f $@
	@resize2fs -M $@

run/%: output/%.img payloads/%.jsonl
	@fc_wrapper --kernel vmlinux-4.20.0 --mem_size 2048 --rootfs python3.ext4 --appfs output/$*.img < payloads/$*.jsonl 2>&1 | tee $@
