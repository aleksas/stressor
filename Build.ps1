$ErrorActionPreference = 'Stop';
Write-Host Starting build

if ($isWindows) {

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll -DeploymentName to-publish

	msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
	Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll -DeploymentName to-publish


} else {

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
	
	[datetime]$stop = ([datetime]::Now).AddMinutes($env:TimeOutMins)
	[bool]$success = $false  

	while(!$success -and ([datetime]::Now) -lt $stop) {
		$project = Invoke-RestMethod -Uri "https://ci.appveyor.com/api/projects/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG" -Headers $headers -Method GET

		$jobToWaitJson = $project.build.jobs | where {$_.name -eq $env:jobToWait}  
		$success = $jobToWaitJson.status -eq "success"
		$jobToWaitId = $jobToWaitJson.jobId;
		if (!$success) {Start-sleep 5}
	}

	if (!$success) {throw "Job `"$env:jobToWait`" was not finished in $env:TimeOutMins minutes"}
	if (!$jobToWaitId) {throw "Unable t get JobId for the job `"$env:jobToWait`""}

	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$jobToWaitId/artifacts/phonology_engine/%2FWin32_x86%2FPhonologyEngine.dll
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$jobToWaitId/artifacts/phonology_engine/%2FWin64_x64%2FPhonologyEngine.dll
	
	########## Build WHEEL ##########
	
	sudo python3 -m pip install --user --upgrade setuptools wheel
	
	python3 setup.py sdist bdist_wheel

}