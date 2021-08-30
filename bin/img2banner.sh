FNAME=$1
SIZE=`identify ${FNAME} | cut -f 3 -d ' '`
LG=`echo ${SIZE} | cut -f 1 -d 'x'`
HT=`echo ${SIZE} | cut -f 2 -d 'x'`
echo $LG x $HT


(( NORM_LG = 1800 ))
(( NREL = 3 ))

(( IREL = LG * 1000 / HT ))
(( BHT = LG / NREL ))
(( BLG = LG ))
(( OFFSET = ( HT - BHT ) / 2 )) 

echo size: $SIZE
echo offset: $OFFSET

echo -n "choose another offset (defaults to current offset): "
read OFFSET1

if [[ $OFFSET1 != "" ]]; then
	(( OFFSET = $OFFSET1 ))
fi 

FNAME_BASE=`echo ${FNAME}|cut -f 1 -d "."`
FNAME_ENDS=`echo ${FNAME}|cut -f 2 -d "."`


if (( LG > NORM_LG )); then
  (( RESIZE = NORM_LG * 1000 / LG ))
  (( BHT = BHT * RESIZE / 1000 ))
  (( BLG = NORM_LG ))
  (( OFFSET = ( OFFSET * RESIZE ) / 1000 ))
  (( RESIZE = RESIZE / 10 ))
  echo resize $RESIZE $IREL $BHT
fi
if (( HT > BHT )); then
  BSIZE="${BLG}x${BHT}+0+${OFFSET}"
  echo bsize $BSIZE
fi

echo convert -resize ${RESIZE}% -crop ${BSIZE} ${FNAME} ${FNAME_BASE}-1.${FNAME_ENDS}
display -resize ${RESIZE}% -crop ${BSIZE} ${FNAME}