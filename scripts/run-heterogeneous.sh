#!/bin/bash
#
# Run the time-energy models for heterogeneous systems
#

SYSTEMS="xu3 tx2"
APPS="ep lv bt sp bs km pf"

cd `dirname ${BASH_SOURCE-$0}`
SCRIPTS_DIR=`pwd`

cd ../data
DATA_DIR=`pwd`

for SYS in $SYSTEMS; do
  . $SCRIPTS_DIR/conf-$SYS.sh
  OUTDIR="$DATA_DIR/model/$SYS"
  rm -rf $OUTDIR
  mkdir -p $OUTDIR
  cd $OUTDIR
  mkdir amdahl-static
  mkdir amdahl-dynamic
  mkdir gustafson-static
  mkdir gustafson-dynamic
  echo "#Val;f;;;;RMSD(f);;;;RMSD(es);;;;" > stats.csv
  echo "#App;Amdahl Static;Amdahl Dynamic;Gustafson Static;Gustafson Dynamic;Amdahl Static;Amdahl Dynamic;Gustafson Static;Gustafson Dynamic;Amdahl Static;Amdahl Dynamic;Gustafson Static;Gustafson Dynamic;" >> stats.csv

  for APP in $APPS; do
    FILE_LITTLE_ONLY=$DATA_DIR/raw/$SYS/static/little_cores/data-$APP.csv
    FILE_BIG_ONLY=$DATA_DIR/raw/$SYS/static/big_cores/data-$APP.csv
    FILE_STATIC_ALL=$DATA_DIR/raw/$SYS/static/all_cores/data-$APP.csv
    FILE_DYNAMIC_ALL=$DATA_DIR/raw/$SYS/dynamic/all_cores/data-$APP.csv
    python $SCRIPTS_DIR/model_heterogeneous.py $N $NL $NB $APFL $APFB $PSYS $APP $FILE_LITTLE_ONLY $FILE_BIG_ONLY $FILE_STATIC_ALL $FILE_DYNAMIC_ALL
  done
  cd ..
done

