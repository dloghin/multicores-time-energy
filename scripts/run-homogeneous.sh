#!/bin/bash
#
# Run the time-energy models for homogeneous systems
#

SYSTEMS="amd arm xeon i7 pi3"
APPS="ep lv bt sp bs km pf cl fe gh"

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
  mkdir amdahl
  mkdir gustafson
  echo "#Val;f;;RMSD(f);;RMSD(es);;" > stats.csv
  echo "#App;Amdahl;Gustafson;Amdahl;Gustafson;Amdahl;Gustafson;" >> stats.csv

  for APP in $APPS; do
    FILE=$DATA_DIR/raw/$SYS/data-$APP.csv
    if ! [ -f "$FILE" ]; then
      continue
    fi
    python3 $SCRIPTS_DIR/model_homogeneous.py $N $APF $PSYS $APP $FILE
  done
  cd ..
done

