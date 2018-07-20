#!/bin/bash

WORD=$1
MODE=$2

stripe() {
sed "s/(//g;s/)//g;s/-//g;s/ō/ou/g;s/ū/uu/g;s/ī/ii/g;s/'//g"
}

trans_jap() {
        /home/arina/./trans ja: $word :en | head -4 | stripe | tr '[:upper:]' '[:lower:]' > trans.log
        kanji=$(sed '1q;d' trans.log)
        pron=$(sed '2q;d' trans.log | sed "s/ //g")
        trans=$(sed '4q;d' trans.log)
        trans=$(echo $trans | tr -cd '[:print:]')
        trans=$(echo $trans | sed "s/\[1m//g;s/\[22m//g")
        hirag=$(bash /home/arina/kanji/2hiragana.sh $pron)
        sound=$(ls /home/arina/kanji/JDIC_Audio_All/*\ $kanji\.mp3 | head -1 | \
                sed 's/\/home\/arina\/kanji\///g')
        echo -ne "$kanji\t$pron\t$trans\t$hirag\t$sound"
}


if [ $MODE = "ja" ]; then
	word=$WORD
	trans_jap
    else
	if [ $MODE = "en" ]; then
		word=$(/home/arina/./trans en: $WORD :ja | sed '5q;d' | stripe | sed "s/ //g" | tr '[:upper:]' '[:lower:]' | \
			tr -cd '[:print:]' | sed "s/\[1m//g;s/\[22m//g")
	else word=$(/home/arina/./trans ru: $WORD :ja | sed '5q;d' | stripe | sed "s/ //g" | tr '[:upper:]' '[:lower:]' | \
                        tr -cd '[:print:]' | sed "s/\[1m//g;s/\[22m//g")
	fi
	trans_jap
    fi

