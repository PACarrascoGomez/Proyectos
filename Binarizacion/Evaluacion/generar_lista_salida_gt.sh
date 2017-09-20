for i in $(ls Dataset/GT/); do
	a=$(echo $i | cut -d "_" -f 1);
	b=$(ls Salida/$a.*);
	echo -e Dataset/GT/$i"\t"$b;
done > lista_salida_gt
