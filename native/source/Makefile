all: install_dependencies compile_x86 compile_x86_64

install_dependencies:
	sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

compile_x86:
	mkdir -p ../../phonology_engine/Linux_x86
	g++ -fPIC -m32 -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp Engine.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
	
compile_x86_64:	
	mkdir -p ../../phonology_engine/Linux_x86_64
	g++ -fPIC -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp Engine.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings

clean:
	rm ../../phonology_engine/Linux_x86/libPhonologyEngine.so
	rm ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so