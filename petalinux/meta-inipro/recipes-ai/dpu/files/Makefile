# makefile for DPU driver (outside the linux kernel tree)
# a typical command for build the driver:
#		make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- KERNELDIR=/path/to/your/kernel
modname:=dpu
obj-m:=$(modname).o
dpu-objs:=dpucore.o dpuext.o

PWD :=$(shell pwd)
#MAKE :=make


KCFLAGS=KCFLAGS="
ifeq ($(DPU_TARGET),1.1)
	KCFLAGS +=-DCONFIG_DPU_v1_1_X
else
	KCFLAGS +=-DCONFIG_DPU_v1_3_0
endif

ifeq ($(ARCH),arm)
	KCFLAGS +=-DSIG_BASE_ADDR=0X4FF00000 -DCACHE_OFF
endif
ifeq ($(ARCH),arm64)
	KCFLAGS +=-DSIG_BASE_ADDR=0X8FF00000
endif

# check the compiler version
GCCV1 := $(shell $(CROSS_COMPILE)gcc -dumpversion | cut -f1 -d. )
GCCV2 := $(shell $(CROSS_COMPILE)gcc -dumpversion | cut -f2 -d. )
GCCV3 := $(shell expr `echo $(GCCV1)"*100+"$(GCCV2) | bc`  )

DT_FLAG := $(shell expr `echo $(GCCV3)` \>= 409)
ifeq ($(DT_FLAG),1)
    KCFLAGS += -Wno-error=date-time -Wno-date-time
endif
KCFLAGS+="

all:
	$(KCFLAGS) $(MAKE) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SRC) M=$(PWD) modules

modules_install:
	$(KCFLAGS) $(MAKE) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) -C $(KERNEL_SRC) M=$(PWD) modules_install

clean:
	rm -rf $(modname).ko *.o *mod* \.*cmd *odule* .tmp_versions

.PHONY: all clean

