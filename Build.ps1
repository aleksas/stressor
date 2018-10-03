$ErrorActionPreference = 'Stop';
Write-Host Starting build

if ($isWindows) {

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll -DeploymentName to-publish

	echo '1'
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	echo '2'
	
	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll -DeploymentName to-publish
	
	echo '3'
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	echo '4'

} else {

	sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

	cd native/source

	mkdir -p ../../phonology_engine/Linux_x86

	g++ -fPIC -m32 -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
	  
	Push-AppveyorArtifact ../../phonology_engine/Linux_x86/libPhonologyEngine.so -FileName phonology_engine/Linux_x86/libPhonologyEngine.so -DeploymentName to-publish

	echo '5'
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	echo '6'
	
	mkdir -p ../../phonology_engine/Linux_x86_64

	g++ -fPIC -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings

	Push-AppveyorArtifact ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -FileName phonology_engine/Linux_x86_64/libPhonologyEngine.so -DeploymentName to-publish

	echo '7'
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	echo '8'

}