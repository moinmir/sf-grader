
output/%.img: functions/%/*
	@truncate -s 500M $@
	@mkfs.ext4 -F $@
	@cptofs -t ext4 -i $@ functions/$*/* /
	@e2fsck -f $@
	@resize2fs -M $@

run/%: output/%.img payloads/%.jsonl
	@fc_wrapper --kernel ../../snapfaas/resources/images/vmlinux-4.20.0 --mem_size 2048 --rootfs python3.ext4 --appfs output/$*.img < payloads/$*.jsonl | tee $@
