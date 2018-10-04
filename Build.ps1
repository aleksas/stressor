param (
	[switch]$build,
	[switch]$test,
	[switch]$after_test,
	[switch]$on_finish
)

$ErrorActionPreference = 'Stop';

if ($isWindows) {
	apt install python3-pip -y
	python3 -m pip install --user --upgrade setuptools wheel nose
} else {
	sudo apt install python3-pip -y
	sudo python3 -m pip install --user --upgrade setuptools wheel nose
}

if ($build) {
	Write-Host Starting build
	
	if ($isWindows) {

		# Build native windows libraries

		msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
		ls phonology_engine
		ls phonology_engine/Win32_x86
		Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll -DeploymentName to-publish
		
		msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
		ls phonology_engine
		ls phonology_engine/Win64_x64
		Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll -DeploymentName to-publish

	} else {

		# Build native linux libraries

		sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

		cd native/source

		mkdir -p ../../phonology_engine/Linux_x86
		g++ -fPIC -m32 -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
		  
		mkdir -p ../../phonology_engine/Linux_x86_64
		g++ -fPIC -g -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings

		cd ../..
		
	}
	
	python setup.py build
}

if ($test){
	Write-Host Starting test
	
	# Install nose tests
	
	# this produces nosetests.xml
	python setup.py nosetests --with-xunit
	
	if ($LastExitCode -ne 0) {
		$host.SetShouldExit($LastExitCode)
	}
}

if ($on_finish){
	Write-Host On Finish
	
	# this uploads nosetests.xml produced in test_script step
	$wc = New-Object 'System.Net.WebClient'
	$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", (Resolve-Path .\nosetests.xml))
}

if ($after_test -and (-NOT $isWindows)){
	Write-Host After Test
	
	# Download VS artifacts
	
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

	# Build WHEEL dsitro
	
	python3 setup.py sdist bdist_wheel
}
