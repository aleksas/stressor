$ErrorActionPreference = 'Stop';
Write-Host Starting build

if ($isWindows) {

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName Win32_x86/PhonologyEngine.dll

	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	
	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName Win64_x64/PhonologyEngine.dll
	
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}

} else {

	sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

	cd native/source

	mkdir -p ../../phonology_engine/Linux_x86

	g++ -fPIC -m32 -g \
	  -I ../include/ \
	  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
	  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
	  -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
	  
	Push-AppveyorArtifact ../../phonology_engine/Linux_x86/libPhonologyEngine.so -FileName Linux_x86/libPhonologyEngine.so

	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	
	mkdir -p ../../phonology_engine/Linux_x86_64

	g++ -fPIC -g \
	  -I ../include/ \
	  Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp \
	  ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp \
	  -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings

	Push-AppveyorArtifact ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -FileName Linux_x86_64/libPhonologyEngine.so

	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}

}