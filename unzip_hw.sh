for f in "$PWD"/*.zip; do
   echo "Unzip $f :";
   unzip $f
   rm $f
done

