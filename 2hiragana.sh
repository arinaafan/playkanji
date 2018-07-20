#!/bin/sh

str=$1

# while read str;
for word in ${str[@]};
  do
    echo $str | sed  " \
s/tt/っt/g; \
s/pp/っp/g; \
s/kk/っk/g; \
s/ss/っs/g; \
s/ wa$/ ha/g; \
s/ wa / ha /g; \
s/shi/し/g; \
s/chi/ち/g; \
s/tsu/つ/g; \
s/kyo/きょ/g; \
s/gyo/ぎょ/g; \
s/kya/きゃ/g; \
s/gya/ぎゃ/g; \
s/kyu/きゅ/g; \
s/gyu/ぎゅ/g; \
s/sha/しゃ/g; \
s/sya/しゃ/g; \
s/shu/しゅ/g; \
s/syu/しゅ/g; \
s/sho/しょ/g; \
s/syo/しょ/g; \
s/cha/ちゃ/g; \
s/chu/ちゅ/g; \
s/che/ちぇ/g; \
s/cho/ちょ/g; \
s/nya/にゃ/g; \
s/nyu/にゅ/g; \
s/nyo/にょ/g; \
s/hya/ひゃ/g; \
s/hyu/ひゅ/g; \
s/hyo/ひょ/g; \
s/byu/びゅ/g; \
s/byo/びょ/g; \
s/rya/りゃ/g; \
s/ryu/りゅ/g; \
s/ryo/りょ/g; \
s/dzu/じゅ/g; \
s/dzi/じ/g; \
s/ka/か/g; \
s/ga/が/g; \
s/ki/き/g; \
s/gi/ぎ/g; \
s/ku/く/g; \
s/gu/ぐ/g; \
s/ke/け/g; \
s/ge/げ/g; \
s/ko/こ/g; \
s/go/ご/g; \
s/sa/さ/g; \
s/za/ざ/g; \
s/ji/じ/g; \
s/su/す/g; \
s/zu/ず/g; \
s/se/せ/g; \
s/ze/ぜ/g; \
s/so/そ/g; \
s/zo/ぞ/g; \
s/ta/た/g; \
s/da/だ/g; \
s/di/ぢ/g; \
s/du/づ/g; \
s/te/て/g; \
s/de/で/g; \
s/to/と/g; \
s/do/ど/g; \
s/na/な/g; \
s/ni/に/g; \
s/nu/ぬ/g; \
s/ne/ね/g; \
s/no/の/g; \
s/ha/は/g; \
s/ba/ば/g; \
s/pa/ぱ/g; \
s/hi/ひ/g; \
s/bi/び/g; \
s/pi/ぴ/g; \
s/fu/ふ/g; \
s/bu/ぶ/g; \
s/pu/ぷ/g; \
s/he/へ/g; \
s/be/べ/g; \
s/pe/ぺ/g; \
s/ho/ほ/g; \
s/bo/ぼ/g; \
s/po/ぽ/g; \
s/ma/ま/g; \
s/mi/み/g; \
s/mu/む/g; \
s/me/め/g; \
s/mo/も/g; \
s/ya/や/g; \
s/yu/ゆ/g; \
s/yo/よ/g; \
s/ra/ら/g; \
s/ri/り/g; \
s/ru/る/g; \
s/re/れ/g; \
s/ro/ろ/g; \
s/wa/わ/g; \
s/wi/ゐ/g; \
s/we/ゑ/g; \
s/wo/を/g; \
s/ja/じゃ/g; \
s/ju/じゅ/g; \
s/jo/じょ/g; \
s/va/ゔぁ/g; \
s/vi/ゔぃ/g; \
s/vu/ゔ/g; \
s/ve/ゔぇ/g; \
s/vo/ゔぉ/g; \
s/n/ん/g; \
s/m/ん/g; \
s/a/あ/g; \
s/i/い/g; \
s/u/う/g; \
s/e/え/g; \
s/o/お/g"
done

