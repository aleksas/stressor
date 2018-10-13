param (
	[switch]$init,
	[switch]$build,
	[switch]$test,
	[switch]$after_test,
	[switch]$on_finish,
	[switch]$upload
)

#$ErrorActionPreference = 'Stop';

if ($init) {

	Write-Host Initializing

	if ($isWindows) {
		python -m pip install --upgrade pip setuptools wheel nose
	} else {
		sudo apt install python-pip -y	
		python -m pip install --user --upgrade pip setuptools wheel nose twine
	}
}

if ($build) {

	Write-Host Starting build
	
	if ($isWindows) {

		# Build native windows libraries
		if($env:PLATFORM -eq 'x32') {
			msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x86 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
			Push-AppveyorArtifact ./phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll -DeploymentName to-publish
		} else { # x64
			msbuild .\native\source\.VS2017\PhonologyEngine.sln /property:Platform=x64 /p:Configuration=Release  /verbosity:minimal /logger:"C:\Program Files\AppVeyor\BuildAgent\Appveyor.MSBuildLogger.dll"
			Push-AppveyorArtifact ./phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll -DeploymentName to-publish
		}

	} else {

		# Build native linux libraries
		# sudo apt-get install -y libc6-dev-i386 gcc-multilib g++-multilib

		cd native/source

		# -g0 strips debug info, -g adds debug info

		if($env:PLATFORM -eq 'x32') {
			mkdir -p ../../phonology_engine/Linux_x86
			g++ -fPIC -m32 -g0 -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp Engine.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86/libPhonologyEngine.so -Wno-write-strings
			
			Push-AppveyorArtifact ./phonology_engine/Linux_x86/libPhonologyEngine.so -FileName phonology_engine/Linux_x86/libPhonologyEngine.so -DeploymentName to-publish
		} else { # x64
			mkdir -p ../../phonology_engine/Linux_x86_64
			g++ -fPIC -g0 -I ../include/ Transkr.cpp transcrLUSS.cpp Skiemen.cpp Kircdb.cpp fv2id.cpp ArKirciuoti.cpp Engine.cpp strtokf.cpp stringWithLetterPosition.cpp TextNormalization.cpp -shared -o ../../phonology_engine/Linux_x86_64/libPhonologyEngine.so -Wno-write-strings
			
			Push-AppveyorArtifact ./phonology_engine/Linux_x86_64/libPhonologyEngine.so -FileName phonology_engine/Linux_x86_64/libPhonologyEngine.so -DeploymentName to-publish
		}
		cd ../..
		
	}
	
	python setup.py build
	
}

if ($test) {

	Write-Host Starting test
	
	# this produces nosetests.xml
	if ($isWindows) {
		cmd /c python setup.py nosetests --with-xunit --verbosity=2 2`>`&1
	} else {
		python setup.py nosetests --with-xunit --verbosity=2
	}
	
	if ($LastExitCode -ne 0) {
		$lec = $LastExitCode
		echo "LastExitCode After: $lec"
		$host.SetShouldExit($lec)
	}
		
}

if ($after_test -and $isLinux -and $env:PLATFORM -eq 'x64') {

	Write-Host After Test
	
	# Download VS artifacts
	
	$env:previousJob = 'Image: Visual Studio 2017'
	
	$headers = @{
		"Authorization" = "Bearer $ApiKey"
		"Content-type" = "application/json"
	}
	
	[bool]$success = $false  

	$project = Invoke-RestMethod -Uri "https://ci.appveyor.com/api/projects/$env:APPVEYOR_ACCOUNT_NAME/$env:APPVEYOR_PROJECT_SLUG" -Headers $headers -Method GET

	$previousJobJson = $project.build.jobs | where {$_.name -eq $env:previousJob}  
	$success = $previousJobJson.status -eq "success"
	$previousJobId = $previousJobJson.jobId;

	if (!$previousJobId) {throw "Unable t get JobId for the job `"$env:previousJob`""}

	mkdir -p phonology_engine/Win32_x86
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$previousJobId/artifacts/phonology_engine/Win32_x86/PhonologyEngine.dll -FileName phonology_engine/Win32_x86/PhonologyEngine.dll

	mkdir -p phonology_engine/Win64_x64
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$previousJobId/artifacts/phonology_engine/Win64_x64/PhonologyEngine.dll -FileName phonology_engine/Win64_x64/PhonologyEngine.dll

	mkdir -p phonology_engine/Linux_x86
	Start-FileDownload  https://ci.appveyor.com/api/buildjobs/$previousJobId/artifacts/phonology_engine/Linux_x86/PhonologyEngine.dll -FileName phonology_engine/Linux_x86/libPhonologyEngine.so

	# Build WHEEL dsitro

	python setup.py sdist bdist_wheel

}

if ($on_finish) {

	Write-Host On Finish
	
	# this uploads nosetests.xml produced in test_script step
	$wc = New-Object 'System.Net.WebClient'
	$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", (Resolve-Path .\nosetests.xml))
	
}

if ($upload -and $isLinux) {

	Write-Host Upload

@"
[distutils]
index-servers =
    pypi
[pypi]
username: aleksas
password: $env:PYPI_PASSWORD
"@ | Out-File ~/.pypirc -Force -Encoding ascii

	python -m twine upload --verbose --skip-existing dist/*.whl

}
