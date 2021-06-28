#!/usr/bin/bash
PCBFILE=board_x

kikit modify references --hide -p '.*' ${PCBFILE}.kicad_pcb
pcbdraw -s ../../pd_picsimlab_libs/picsimlab.json -l ../../pd_picsimlab_libs/ ${PCBFILE}.kicad_pcb ${PCBFILE}.svg

ow=`xmlstarlet  sel --omit-decl -N x=http://www.w3.org/2000/svg  -t -v "//x:svg[@width]/@width"  ${PCBFILE}.svg 2>/dev/null | rev | cut -c3- | rev` 
oh=`xmlstarlet  sel --omit-decl -N x=http://www.w3.org/2000/svg  -t -v "//x:svg[@height]/@height"  ${PCBFILE}.svg 2>/dev/null | rev | cut -c3- | rev` 
nw=`echo "($ow*96.0/2.54)*1.5" | bc`
nh=`echo "($oh*96.0/2.54)*1.5" | bc`
LC_ALL=C printf -v nw %.0f $nw
LC_ALL=C printf -v nh %.0f $nh
echo -e "size  $nw x $nh \n"
#xmlstarlet ed --omit-decl -N x=http://www.w3.org/2000/svg  -u "//x:svg[@width]/@width" -v "$nw" ${PCBFILE}.svg  | \
#xmlstarlet ed --omit-decl -N x=http://www.w3.org/2000/svg  -u "//x:svg[@height]/@height" -v "$nh"  > ${PCBFILE}_.svg

#edicao manual
width="448"
height="491"
viewBox="0 0 31133.53 34147.547"

xmlstarlet ed --omit-decl -N x=http://www.w3.org/2000/svg  -u "//x:svg[@width]/@width" -v "$width" ${PCBFILE}.svg  | \
xmlstarlet ed --omit-decl -N x=http://www.w3.org/2000/svg  -u "//x:svg[@viewBox]/@viewBox" -v "$viewBox"  | \
xmlstarlet ed --omit-decl -N x=http://www.w3.org/2000/svg  -u "//x:svg[@height]/@height" -v "$height"  > board_.svg

sed -i 's/translate(-20461, -13461)/translate(-20425.834,-13369.134)/g' board_.svg

#put background
sed -i 's/PcbDraw<\/desc>/PcbDraw<\/desc>\n<rect y="-5%" x="-5%" width="110%" height="110%" fill="#f0f0f0" \/>/g' board_.svg 

#put text top layer (ICs description)
#head -n -1 board_.svg > temp.svg
#mv temp.svg board_.svg
#cat text.layer >> board_.svg
#echo "</svg>" >> board_.svg
