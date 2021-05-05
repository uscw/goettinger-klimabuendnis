SIZE=`identify $1 | cut -f 3 -d ' '`
LG=`echo ${SIZE} | cut -f 1 -d 'x'`
HT=`echo ${SIZE} | cut -f 2 -d 'x'`

echo $SIZE
(( NREL = 3 ))

(( IREL = LG / HT ))

(( BHT = LG / NREL ))

(( BLG = LG ))

(( OFFSET = ( HT - BHT ) / 2 )) 
if (( IREL < BHT )); then
  BSIZE="${BLG}x${BHT}+0+${OFFSET}"
  echo $BSIZE
fi

display -crop $BSIZE $1
