TSV_INPUT := blocked_ip.tsv
CONF_FILES := $(TSV_INPUT:.tsv=.conf)

all: $(CONF_FILES)

$(CONF_FILES): $(TSV_INPUT) convert-tsv-to-conf.py
	python convert-tsv-to-conf.py $(TSV_INPUT) $(CONF_FILES)

clean:
	rm -f $(CONF_FILES)

.PHONY: all clean
