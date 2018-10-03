$ErrorActionPreference = 'Stop';
Write-Host Starting build

if ($isWindows) {

	######## Build native windows libraries ##########

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll -DeploymentName to-publish

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll -DeploymentName to-publish

} else {

	######## Build native linux libraries ##########

	sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

	cd native/source

	mkdir -p ../../phonology_engine/Linux_x86

	g++ -fPIC -m32 -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
	  
	mkdir -p ../../phonology_engine/Linux_x86_64

	g++ -fPIC -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings

	cd ../..
	
	######## Download VS artifacts ##########
	
	$env:jobToWait = 'Image: Visual Studio 2017'
	
	$headers = @{
		"Authorization" = "Bearer $ApiKey"
		"Content-type" = "application/json"
	}
	
	[bool]$success = $false  

	$project = Invoke-RestMethod -Uri "https://ci.appveyor.com/api/projects/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG" -Headers $headers -Method GET

	$jobToWaitJson = $project.build.jobs | where {$_.name -eq $env:jobToWait}  
	$success = $jobToWaitJson.status -eq "success"
	$jobToWaitId = $jobToWaitJson.jobId;

	if (!$jobToWaitId) {throw "Unable t get JobId for the job `"$env:jobToWait`""}

	mkdir -p phonology_engine/Win32_x86
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$jobToWaitId/artifacts/phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll

	mkdir -p phonology_engine/Win64_x64
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$jobToWaitId/artifacts/phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll
	
	echo 'APPVEYOR_BUILD_NUMBER:' + $env:APPVEYOR_BUILD_NUMBER
	echo 'APPVEYOR_BUILD_VERSION:' + $env:APPVEYOR_BUILD_VERSION

	ls phonology_engine
	
	########## Build WHEEL ##########
	
	sudo apt install python3-pip -y
	sudo python3 -m pip install --user --upgrade setuptools wheel
	
	python3 setup.py sdist bdist_wheel

}