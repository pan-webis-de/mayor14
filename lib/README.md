POS tagging
===========

Para etiquetar las categorías gramaticales usamos un código en java que leé 
los documentos y los etiqueta de forma automática. Para lograr esto hay que 
hacer lo siguiente:

Requisitos
----------

* Java a

El siguiente link contiene instrucciones para su instalación en Ubuntu:

https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get

Instalar las librerias de CoreNLP de Stanford
---------------------------------------------

En el directorio de `authorid` ejecutar para conseguir las librerias

    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip
    unzip stanford-corenlp-full-2015-01-29.zip
    cp stanford-corenlp-full-2015-01-29/stanford-corenlp-3.5.1.jar lib/
    cp stanford-corenlp-full-2015-01-29/stanford-corenlp-3.5.1-models.jar lib/
    wget http://nlp.stanford.edu/software/stanford-spanish-corenlp-2015-01-08-models.jar
    mv stanford-spanish-corenlp-2015-01-08-models.jar lib

Compilación
-----------

Opcionalmente se puede borrar las librerias
    
    rm -r stanford-corenlp-full-2015-01-29
    rm -r stanford-corenlp-full-2015-01-29.zip

Para compilar nuestró código se hace lo siguiente en el directorio 
`authorid/src/java`

    javac -classpath ../../lib/*:* SpanishTagger.java
    javac -classpath ../../lib/*:* EnlgishTagger.java

Ejecutar/etiquetar
------------------

Para etiquetar por ejemplo un directorio con textos en español hacer lo siguiente:

    java -classpath ../../lib/*:. SpanishTagger ../../data/pan15_train/spanish

Al finalizar debe haber archivos extra con la extensión `_tag`.


