$ErrorActionPreference = 'Stop';
Write-Host Starting build

if (!$isWindows) {

	echo '7'
	foreach ($artifactName in $artifacts.keys) {
	  echo $artifacts[$artifactName]
	}
	echo '8'

	sudo python3 -m pip install --user --upgrade setuptools wheel
	
	python3 setup.py sdist bdist_wheel
	
	ls

}