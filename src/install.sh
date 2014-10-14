#!/bin/bash
# Instalace aplikace
# Cílová složka
TDIR="/opt/gnuClassConf";
# Pokud instalace probíhá ze stejné složky, jako je umístění aplikace
if [[ "$PWD" == "$TDIR" ]];then
	echo "Cílová složka je stejná jako instalační";
	echo "Zkontrolujte své umístění";
	exit 10;
else
	if [[ -d "$TDIR" ]];then
		# Složka už existuje, kopíruji vše až na konfigurační soubory
		# Pokud konfigurační soubory focus/installed.cfg, configuration/shared
		# a configuration/interfaces existují, nepřepisovat
		d=`mktemp -d`;
		echo "Zálohuji konfiguraci";
		mv "$TDIR/configuration/interfaces" $d;
		mv "$TDIR/configuration/shared" $d;
		mv "$TDIR/focus/installed.cfg" $d;
		rm -r "$TDIR";
		echo "Kopíruji soubory";
		cp -r "$PWD" "$TDIR";
		echo "Obnovuji konfiguraci";
		cat "$d/interfaces" > "$TDIR/configuration/interfaces";
		cat "$d/shared" > "$TDIR/configuration/shared";
		cat "$d/installed.cfg" > "$TDIR/focus/installed.cfg";
		rm -r $d;
	else
		# Zkopírovat vše a přepsat konfigurační soubory na čisto
		echo "Kopíruji";
		cp -r "$PWD" "$TDIR";
		echo "Připravuji konfigurační soubory";
		cat "$PWD/configuration/interfaces_cl" > "$TDIR/configuration/interfaces";
		cat "$PWD/configuration/shared_cl" > "$TDIR/configuration/shared";
		cat "$PWD/focus/installed_cl.cfg" > "$TDIR/focus/installed.cfg";
		# Čištění logu
		echo "" > "$TDIR/data/work_logs.log"
	fi
fi
