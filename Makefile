FUNCTIONS=start_assignment gh_repo go_grader grades generate_report
OUTPUTS=$(patsubst %, output/%.img, $(FUNCTIONS))
RUNS=$(patsubst %, run/%, $(FUNCTIONS))

.PHONY: all
all: $(OUTPUTS) #$(RUNS)

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
	@singlevm --mem_size 256 --kernel vmlinux-4.20.0 --rootfs python3.ext4 --appfs output/$*.img < payloads/$*.jsonl
	@touch $@

.PHONY: clean
clean:
	rm -f $(OUTPUTS) $(RUNS)
