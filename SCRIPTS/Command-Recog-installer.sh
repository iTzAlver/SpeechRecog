#!/bin/bash
echo Intalando dependencias...
sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev autoconf libtool automake bison
echo Dependencias instaladas.
echo Creando carpeta para Sphinx...
mkdir sphinx
cd sphinx
git clone https://github.com/cmusphinx/sphinxbase
git clone https://github.com/cmusphinx/pocketsphinx
cd sphinxbase
./autogen.sh
./configure
make
sudo make install
cd ..
cd pocketsphinx
./autogen.sh
./configure
make
sudo make install
cd ..
echo Sphinxbase y pocketsphinx instalados.
pip install --upgrade pip setuptools wheel
pip install --upgrade pocketsphinx
echo Librerías python instaladas.
git clone https://github.com/iTzAlver/SpeechRecog
cd SpeechRecog
cd DICT
tar -xfz cmusphinx-es-5.2.tar.gz
gzip -d es-20.lm.gz
mv es-20.lm.gz ~/.local/lib/python2.7/site-packages/pocketsphinx/model/es-20.lm.bin
mv es.dict ~/.local/lib/python2.7/site-packages/pocketsphinx/model/es.dict
cd cmusphinx-es-5.2
mv voxforge_es_sphinx.cd_ptm_4000 ~/.local/lib/python2.7/site-packages/pocketsphinx/model/es-es
echo Modelo español copiado correctamente.
